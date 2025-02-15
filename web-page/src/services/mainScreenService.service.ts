import { Injectable } from '@angular/core';

import { MainScreenOptions } from 'src/enum/screen-type'

@Injectable({
  providedIn: 'root'
})
export class MainScreenService {

    selectedScreen: MainScreenOptions = MainScreenOptions.USERS

    constructor() 
    {
    }

    setScreenType(name: string)
    {
        if(name == 'Users')
        {
            this.selectedScreen = MainScreenOptions.USERS;
        }
        else if(name == 'Locations')
        {
            this.selectedScreen = MainScreenOptions.BUILDINGS;
        }
        else if(name == 'Calendars')
        {
            this.selectedScreen = MainScreenOptions.CALENDAR;
        }
    }

    isUsersSelected()
    {
        return this.selectedScreen == MainScreenOptions.USERS;
    }

    isLocationsSelected()
    {
        return this.selectedScreen == MainScreenOptions.BUILDINGS;
    }

    isCalendarSelected()
    {
        return this.selectedScreen == MainScreenOptions.CALENDAR;
    }

}