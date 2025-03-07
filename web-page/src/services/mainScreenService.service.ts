import { Injectable } from '@angular/core';

import { MainScreenOptions } from 'src/enum/screen-type'

@Injectable({
  providedIn: 'root'
})
export class MainScreenService {

    selectedScreen: MainScreenOptions = MainScreenOptions.CALENDAR

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
        else if(name == 'Calendar')
        {
            this.selectedScreen = MainScreenOptions.CALENDAR;
        }
        else if(name == 'Marks')
        {
            this.selectedScreen = MainScreenOptions.MARKS;
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

    isMarkTableSelected()
    {
        return this.selectedScreen == MainScreenOptions.MARKS;
    }

}