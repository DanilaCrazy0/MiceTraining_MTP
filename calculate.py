def transport_forecast(data):
    """
    {'housingClass': 'low',
    'residentialArea': '12344',
    'officeArea': '1325435',
    'workingPopulation': 57,
    'otItRatio': 70,
    'carOccupancy': 1.2,
    'peakLoadLive': 10,
    'peakLoadOffice': 35,
    'stations': [{'stationName': 'а',
                'passengerFlowMorning': '123',
                'passengerFlowEvening': '444',
                'stationCapacity': '123412'}],
    'roads': [{'roadName': 'ПП',
            'roadIntensity': '31241234',
            'roadScore': '5'}]}"""
    # коэффициенты и данные
    S1 = int(data['residentialArea'])
    S2 = int(data['officeArea'])

    if data["housingClass"] == 'low':
        e1 = 25
    elif data["housingClass"] == 'medium':
        e1 = 35
    else:
        e1 = 45
    e2 = 35
    residental_flow = S1 / e1
    officeFlow = S2 / e2

    workingPopulation = data['workingPopulation'] * 0.01
    ItRatio = 1 - data['otItRatio'] * 0.01
    otRatio = data['otItRatio'] * 0.01
    carOccupancy = data['carOccupancy']
    peakLoadLive = data['peakLoadLive'] * 0.01
    peakLoadOffice = data['peakLoadOffice'] * 0.01

    # Расчеты
    forecast = {
        'stations': [],
        'roads': []
    }

    for station in data['stations']:
        morning_pick_usual = float(station['passengerFlowMorning']) * 1000
        capacity_of_station = float(station['stationCapacity']) * 1000
        new_pick = morning_pick_usual + peakLoadLive * workingPopulation * otRatio * residental_flow + peakLoadOffice * otRatio * officeFlow
        forecast['stations'].append({'stationName': station['stationName'],
                                     'increaseMorningPick': round(new_pick, 2),
                                     'bandwidthReserve': round(capacity_of_station-new_pick, 2)})

    sum_score = 0
    for elem in data['roads']:
        sum_score += int(elem['roadScore'])

    for road in data['roads']:
        relative_score = int(road['roadScore']) / sum_score
        morning_flow_auto = (workingPopulation * ItRatio * peakLoadLive * residental_flow + peakLoadOffice * ItRatio * officeFlow) / carOccupancy
        new_pick = morning_flow_auto * relative_score
        capacity_of_road = int(road['roadIntensity']) / (int(road['roadScore']) * 0.1)
        forecast['roads'].append({'roadName': road['roadName'],
                                'increaseMorningPick': round(new_pick, 2),
                                'bandwidthReserve': round(capacity_of_road - new_pick)})

    return forecast
