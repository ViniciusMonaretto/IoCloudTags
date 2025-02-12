import { Component, OnInit } from '@angular/core';
import { UserService } from 'src/services/userService.service';
import { User } from '../../models/user'

@Component({
  selector: 'user-page',
  templateUrl: './user-page.component.html',
  styleUrls: ['./user-page.component.scss']
})
export class UserPageComponent implements OnInit {

  constructor(private UserService: UserService) { 
    this.users = []
  }

  users: Array<User>

  ngOnInit(): void {
    
    this.getUsers()
  }

  getUsers()
  {
    return this.UserService.requestData().subscribe((response: any) => {
      this.users = []
      for(let userInfo of response)
      {
        let info = userInfo.replace(/'/g, '"')
        info = info.replace('None' , "null")
        info = JSON.parse(info)
        this.users.push(new User(info["Name"], info["Email"], info["PhoneNumber"], info["Type"], info["Rfid"]))
      }
    })
  }

}
