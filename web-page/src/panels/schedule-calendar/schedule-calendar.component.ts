import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { CalendarOptions, EventInput } from '@fullcalendar/core';
import dayGridPlugin from '@fullcalendar/daygrid';
import interactionPlugin from '@fullcalendar/interaction';
import timeGridPlugin from '@fullcalendar/timegrid';
import { ServerConnectionService } from 'src/services/serverConection.service';

import { Location } from 'src/models/location';
import { User } from 'src/models/user';
import { Event } from 'src/models/event';
import { EventDialogComponent } from 'src/components/event-dialog/event-dialog.component';

@Component({
  selector: 'schedule-calendar',
  templateUrl: './schedule-calendar.component.html',
  styleUrls: ['./schedule-calendar.component.scss']
})

export class ScheduleCalendarComponent implements OnInit {

    events: Array<EventInput> = []
    locations: Array<Location> = []
    users: Array<User> = []
    selectedUser: User|null = null
    selectedLocation: Location|null = null

    constructor(public dialog: MatDialog, public serverConnection: ServerConnectionService) { }

    ngOnInit(): void {
      this.serverConnection.requestDataLocation().subscribe((response) => {
        this.locations = []
        for(let locationInfo of response)
        {
          let info = locationInfo.replace(/'/g, '"')
          info = info.replace('None' , "null")
          info = JSON.parse(info)
          this.locations.push(new Location(info["Name"], info["Block"], info["Sector"], info["GatewayUuid"], info["AdminUserId"], info["Id"]))
        }
      })
      
      if(this.serverConnection.hasAdminAccess())
      {
        this.serverConnection.requestDataUser().subscribe((response) => {
          this.users = []
          for(let userInfo of response)
          {
            let info = userInfo.replace(/'/g, '"')
            info = info.replace('None' , "null")
            info = JSON.parse(info)
            this.users.push(new User(info["Name"], info["Email"], info["PhoneNumber"], info["Type"], info["Rfid"], info["id"]))
          }
        })
      }
      
    }

    validForm()
    {
      return this.selectedUser != null || this.selectedLocation != null
    }

    requestEvents()
    {
      this.serverConnection.getEvents(this.selectedUser?.Id, this.selectedLocation?.Id).subscribe((result)=>{
          this.events = []
          for(let eventInfo of result)
          {
            let info = eventInfo.replace(/'/g, '"')
            info = info.replace('None' , "null")
            info = JSON.parse(info)
            this.events.push(new Event(info["LocationId"], info["UserId"],new Date(info["BeginDate"]),new Date(info["EndDate"])))
          }
        })
    }
    

    calendarOptions: CalendarOptions = {
      initialView: 'timeGridWeek', // Mostra a semana por padrão
      locale: 'pt-br', // Define o idioma para português
      plugins: [dayGridPlugin, interactionPlugin, timeGridPlugin], // Plugins necessários
      headerToolbar: {
        left: 'prev,next today',
        center: 'title',
        right: 'dayGridMonth,timeGridWeek,timeGridDay'
      },
      buttonText: { 
        today: 'Hoje', 
        month: 'Mês', 
        week: 'Semana', 
        day: 'Dia', 
        list: 'Lista' 
      },
      events: [
        { title: 'Reunião de equipe', start: '2025-02-17T10:00:00', end: '2025-02-17T13:00:00' },
        { title: 'Entrega do projeto', start: '2025-02-20T15:00:00' }
      ],
      dateClick: this.handleDateClick.bind(this)
    };

    handleDateClick(arg: any) {
      const dialogRef = this.dialog.open(EventDialogComponent, {
        data: {user: {}, begin: arg.dateStr,
        callback: (event: Event) =>
        {
          console.log('Add new User');
          this.serverConnection.addEvent(event).subscribe((result)=>{
            this.requestEvents()
          })
        }},
      });
    }
  }