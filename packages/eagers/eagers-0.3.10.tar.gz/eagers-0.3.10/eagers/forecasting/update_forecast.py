from datetime import timedelta

from eagers.basic.get_data import get_data
from eagers.forecasting.arima import arima
from eagers.forecasting.arma import arma
from eagers.forecasting.error_as_rv import apply_forecast_error
from eagers.forecasting.surface_forecast import surface_forecast
from eagers.forecasting.weather_forecast import weather_forecast


def update_forecast(options, date, test_data, subnet, perturber=None):
    """Update forecast using any of the following forecasting
    algorithms:
    Perfect     Perfect forecast. Requires future data, and therefore is
                only available in simulation mode.
    Surface     Surface forecast.
    ARMA        AutoRegressive Moving Average forecast.
    ARIMA       AutoRegressive Integrated Moving Average forecast.
    ANN         Artificial Neural Network forecast.
    
    Positional arguments:
    options - (Optimoptions) Project options.
    date - (list of timestamp) Timestamps for which a forecast is
        requested.
    test_data 
    subnet - (dict) Network data.

    Keyword arguments:
    perturber - (Perturber) (Default: None) Perturber for applying
        forecast error.
    """
    hist_prof = test_data['hist_prof']
    # Period of repetition (1 = 1 day). This is how far back the
    # forecasting methods are able to see. It is irrelevant if the
    # forecast is perfect.
    
    if not options['forecast'] in ['perfect','error_as_rv']:
        #TODO replace with observer history
        d0 = date[0] - timedelta(hours = 24+options['resolution'])
        prev_date = [d0 + timedelta(hours = i*options['resolution']) for i in range(round(24/options['resolution'],0)+1)]
        prev_data = get_data(test_data,prev_date,subnet['network_names'])
    forecast = {}
    forecast['timestamp'] = date
    if options['forecast'] != 'arima' and not options['forecast'] in ['perfect','error_as_rv']:
        forecast['weather'] = weather_forecast(test_data,prev_data, hist_prof, date)
    if options['forecast'] == 'arma':
        forecast['demand'] = arma(date, prev_data)
    elif options['forecast'] == 'arima':
        forecast = arima(date, prev_data, options)
    elif options['forecast'] == 'neural_net':
        pass
    #TODO # create neural network forecasting option
    elif options['forecast'] == 'surface':
        forecast['demand'] = surface_forecast(prev_data, hist_prof['demand'], date, forecast['weather']['t_dryb'],[])
    elif options['forecast'] in ['perfect','error_as_rv']:
        forecast = apply_forecast_error(
            get_data(test_data, date, subnet['network_names']), perturber
        )
    elif options['forecast'] == 'building':
        pass
    else:
        raise RuntimeError('Forecast option not recognized.')
    ### Make first hour forecast "perfect"
    # make_perfect(forecast,options,test_data,date,subnet)
    if options['spin_reserve']:
        if 'demand' in forecast:
            #TODO update this
            forecast['sr_target'] += options['spin_reserve_perc'] / 100 * sum(
                forecast['demand']['e'], 2)
    return forecast


def make_perfect(forecast,options,test_data,date,subnet):
    #Make first step of forecast perfect:
    if options['method'].lower() == 'dispatch' and len(date) > 1:
        next_data = get_data(test_data, date[0], subnet['network_names'])
        for k in next_data:
            if isinstance(next_data[k], dict):
                for s_i in next_data[k]:
                    forecast[k][s_i][0] = next_data[k][s_i][0]
            else:
                forecast[k][0] = next_data[k][0]
