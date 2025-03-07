import { Component, OnInit } from '@angular/core';
import { Mark } from 'src/models/mark';
import { Location } from 'src/models/location';
import { User } from 'src/models/user';
import { ServerConnectionService } from 'src/services/serverConection.service';

@Component({
  selector: 'marks-table',
  templateUrl: './marks-table.component.html',
  styleUrls: ['./marks-table.component.scss']
})
export class MarksTableComponent implements OnInit {

  marks: Array<Mark> 
  locations: Array<Location> = []
  users: Array<User> = []
  selectedUser: User | null = null
  selectedLocation: Location | null = null

  selectedDate: Date | null = null


  getByUser = false

  constructor( public serverConnection: ServerConnectionService) {
    this.marks = []
   }

  ngOnInit(): void {
    setTimeout(
      ()=>
      {
        this.serverConnection.requestDataLocation().subscribe((response) => {
          this.locations = []
          for(let locationInfo of response)
          {
            let info = locationInfo.replace(/'/g, '"')
            info = info.replace('None' , "null")
            info = JSON.parse(info)
            this.locations.push(new Location(info["Name"], info["Block"], info["Sector"], info["GatewayUuid"], info["AdminUserId"], info["id"]))
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
      }, 500);
  }

  setTime(event: any, selectedDateTime: Date | null) {
    if (selectedDateTime) {
      const [hours, minutes] = event.target.value.split(':');
      selectedDateTime.setHours(parseInt(hours, 10), parseInt(minutes, 10));
    }
  }

  toggleUserSelect()
  {
    this.getByUser = !this.getByUser
    if(this.getByUser)
    {
      this.selectedLocation = null
    }
    else
    {
      this.selectedUser = null
    }
  }

  validForm()
  {
    return this.selectedLocation || this.selectedUser
  }

  requestMarks()
  {
    this.serverConnection.getTagMark(this.selectedUser?.Id, this.selectedLocation?.Id, this.selectedDate?.toISOString()).subscribe((response)=>{
      this.marks = []
      for(let userInfo of response)
      {
        let info = userInfo.replace(/'/g, '"')
        info = info.replace('None' , "null")
        info = JSON.parse(info)
        let userSelected = this.users.find(x=>x.Id == info["UserId"])
        let locationSelected = this.locations.find(x=>x.Id == info["LocationId"])
        if(userSelected && locationSelected)
        {
          this.marks.push(new Mark(userSelected, locationSelected, new Date(info["Timestamp"]), info["Id"]))
        }
        
      }
    })
  }

}
