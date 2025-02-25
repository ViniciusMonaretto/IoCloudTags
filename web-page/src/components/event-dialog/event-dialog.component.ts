import { Component, Inject, OnInit } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { Event } from 'src/models/event';
import { User } from 'src/models/user';
import { Location } from 'src/models/location';

@Component({
  selector: 'event-dialog',
  templateUrl: './event-dialog.component.html',
  styleUrls: ['./event-dialog.component.scss']
})
export class EventDialogComponent implements OnInit {

  eventModel: Event = new Event(0, 0, new Date(), new Date())
  users: Array<User> = []
  locations: Array<Location> = []

  constructor(public dialogRef: MatDialogRef<EventDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any
  ) {
    this.users = data.users;
    this.locations = data.locations

    var dateBegin = new Date(data.begin)
    var dateEnd = new Date(data.begin)
    dateEnd.setMinutes(dateEnd.getMinutes() + 30);
    this.eventModel.BeginDate = dateBegin
    this.eventModel.EndDate = dateEnd
  }

  ngOnInit(): void {
  }

  getLocationData()
  {
    return {
      "LocationId": this.eventModel.LocationId,
      "BeginDate": this.eventModel.BeginDate,
      "EndDate": this.eventModel.EndDate,
      "UserId": this.eventModel.UserId,
      "Id": this.eventModel.Id
    }
  }

  validForm()
  {
    return this.eventModel.LocationId != 0 &&
           this.eventModel.UserId != 0 
  }

  onAddCLick(): void{
    this.data.callback(this.getLocationData())
    this.dialogRef.close();
  }

  setTime(event: any, selectedDateTime: Date) {
    if (selectedDateTime) {
      const [hours, minutes] = event.target.value.split(':');
      selectedDateTime.setHours(parseInt(hours, 10), parseInt(minutes, 10));
    }
  }

  onCancel(): void {
    this.dialogRef.close();
  }

}
