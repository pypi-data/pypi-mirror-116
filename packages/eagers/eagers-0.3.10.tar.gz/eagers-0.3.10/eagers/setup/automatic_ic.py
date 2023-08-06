from eagers.basic.find_gen_node import find_gen_node
from eagers.basic.get_data import get_data
from eagers.basic.all_demands import all_demands, add_min_building_demand, subtract_renewable
from eagers.basic.constrain_min_max import constrain_min_max
from eagers.extras import bplus_forecast_dr_capacity
from eagers.solver.test_min_cases import test_min_cases
from eagers.solver.dispatch_step import building_forecast_now
from eagers.simulate.renewable_output import renewable_output
from eagers.forecasting.hydro_forecast import hydro_forecast
from eagers.update.update_matrices_step import update_matrices_step
from eagers.basic.marginal_cost import net_marginal_cost
from eagers.basic.best_eff import best_eff


def automatic_ic(gen,building,fluid_loop,market, subnet, date, one_step, options, test_data, building_observer, scale_cost):
    """Flag values:
    0 -- Standard operation.
    1 -- No feasible combination.
    """
    data_t0 = get_data(test_data, date, subnet['network_names'])
    if 'weather' in data_t0 and 'dir_norm_irr' in data_t0['weather']:
        data_t0['renewable'] = []
        for g in gen:
            if g['type'] in ('Renewable', 'Solar', 'Wind') and g['enabled']:
                gen_network, i_node = find_gen_node(g, subnet)
                location = subnet[gen_network]["location"][i_node]
                gen_output = renewable_output(
                    g, date, data_t0['weather']['dir_norm_irr'], location
                )
            else:
                gen_output = []
            data_t0['renewable'].append(gen_output)
    if building:
        data_t0['building'] = bplus_forecast_dr_capacity(building,building_observer,data_t0['weather'],date)
    else:
        data_t0['building'] = None
    data_t0 = hydro_forecast(data_t0,test_data,date,subnet,[],options)

    demand = all_demands(data_t0,subnet,[0])
    ic_observer = load_ic_observer(gen,fluid_loop,one_step,data_t0)

    # Update marginal cost.
    net_abbrev = [subnet[net]['abbreviation'] for net in subnet['network_names']]
    marginal = net_marginal_cost(gen, net_abbrev, market, None, scale_cost, None, False)
    c_red = best_eff(gen,scale_cost,marginal)  
    sc = [[j[0]] if len(j)>0 else [] for j in scale_cost]
    flt = ic_observer['fluid_loop_temperature']
    flc = ic_observer['fluid_loop_capacitance']
    bat = ic_observer['building_avg_temp']
    fb = building_forecast_now(data_t0['building'],0)
    renewable = {}
    for j in range(len(gen)):
        if gen[j]['type'] in ['Solar','Wind']:
            renewable[gen[j]['name']] = data_t0['renewable'][j][0]
    min_power, max_power = constrain_min_max(gen, 'unconstrained', None, options['resolution'], 0)
    update_matrices_step(gen, market, subnet, options, one_step, fb, renewable, demand,
        sc, marginal, None, options['resolution'], min_power, max_power, None, flt, flc, bat)
    modify_hydro_limits(one_step,subnet,gen,marginal,data_t0)
    add_min_building_demand(data_t0,subnet,demand,[0])
    subtract_renewable(renewable,subnet,demand)
    _, cost, _, disp_comb,_,_,_,_ = test_min_cases(one_step, gen, options, demand, c_red, None,None,None)
    if len(disp_comb) > 0:
        flag = 0
        i_best = cost.index(min(cost))
        ic = disp_comb[i_best]
    else:
        ic = []
        flag = 1
    return ic,data_t0,flag

def load_ic_observer(gen,fluid_loop,one_step,data_t0):
    ic_observer = {}
    n_g = len(gen)
    n_l = len(one_step['organize']['transmission'])
    if not data_t0['building'] is None:
        n_b = len(data_t0['building']['T_avg'][0])
        ic_observer['building_avg_temp'] = [data_t0['building']['T_avg'][0][b] for b in range(n_b)]
    else:
        n_b = 0
        ic_observer['building_avg_temp'] = []
    n_fl = len(fluid_loop['name'])
    ic_observer['fluid_loop_temperature'] = [0 for l in range(n_fl)]
    ic_observer['fluid_loop_capacitance'] = [0 for l in range(n_fl)]
    
    for i in range(n_fl):
        # Set upper and lower bound equal to this temperature to
        # initialize at steady state.
        state = one_step['indices'][n_g+n_l+n_b+i][0][0]
        one_step['lb'][state] = fluid_loop['nominal_return_temperature'][i] - 0.01
        one_step['ub'][state] = fluid_loop['nominal_return_temperature'][i]
        ic_observer['fluid_loop_temperature'][i] = fluid_loop['nominal_return_temperature'][i]
        ic_observer['fluid_loop_capacitance'][i] = fluid_loop['fluid_capacity'][i]*fluid_loop['fluid_capacitance'][i] #Water capacity in kg and thermal capacitance in kJ/kg*K to get kJ/K
    return ic_observer

def modify_hydro_limits(qp,subnet,gen,marginal,data):
    #set hydro gen to produce steady-state, and put substantial price on variation
    gen_names = [gen[i]['name'] for i in range(len(gen))]
    for n in range(qp['network']['electrical']['nodes']):
        equip = subnet['electrical']['equipment'][n]
        req = qp['organize']['balance']['electrical'][n]
        for j in range(len(equip)):
            i = gen_names.index(equip[j])
            if gen[i]['type'] =='HydroStorage':
                states = qp['indices'][i]
                s = states[0]
                outflow = data['hydro']['outflow'][gen[i]['flowcolumn']]
                hydro_power = outflow/gen[i]['stor']['power2flow'] #missing time component?
                #move expected generation to RHS, so that cost penalty can refer to deviations from that power
                qp['beq'][req] -= hydro_power
                qp['lb'][s] -= hydro_power #change in storage for this power output
                qp['ub'][s] -= hydro_power #change in storage for this power output
                #update the equality with NewPower*conversion + spill - Outflow = -nominal PowerGen Flow
                h = qp['organize']['balance']['hydro'].index(n)
                qp['beq'][qp['organize']['hydro_equalities'][h]] = -outflow
                ## assign a cost to deviations
                qp['f'][states[0]] = marginal['e']
                qp['h'][states[0]] = 2*marginal['e']/(.025*hydro_power) #factor of 2 because its solving C = 0.5*x'*H*x + f'*x
