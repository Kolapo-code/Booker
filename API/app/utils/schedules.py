import json

schedules = {
        'days':
            {
                'manday':
                    {
                        'from': '08:00',
                        'to': '18:00'
                    },
                'tuesday':
                    {
                        'from': '08:00',
                        'to': '18:00'
                    },
                'wednesday':
                    {
                        'from': '08:00',
                        'to': '18:00'
                    },
                'thursday':
                    {
                        'from': '08:00',
                        'to': '18:00'
                    },
                'friday':
                    {
                        'from': '08:00',
                        'break':
                            {
                                'from': '12:00',
                                'to': '14:00'
                            },
                        'to': '18:00'
                    },
                'saturday':
                    {
                        'from': '08:00',
                        'to': '12:00'
                    },
                'sunday':
                    {
                        'from': '00:00',
                        'to': '00:00'
                    }
                }
            }

SCHEDULES = json.dumps(schedules)
