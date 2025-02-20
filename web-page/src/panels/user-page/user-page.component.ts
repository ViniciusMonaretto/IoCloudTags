import { Component, OnInit, inject } from '@angular/core';
import { ServerConnectionService } from 'src/services/serverConection.service';
import { User } from '../../models/user'
import { UserDialog } from 'src/components/user-dialog/user-dialog';
import {MatDialog, MatDialogRef} from '@angular/material/dialog';

@Component({
  selector: 'user-page',
  templateUrl: './user-page.component.html',
  styleUrls: ['./user-page.component.scss']
})
export class UserPageComponent implements OnInit {

  constructor(private UserService: ServerConnectionService, private dialog: MatDialog) { 
    this.users = []
  }

  users: Array<User>

  ngOnInit(): void {
    
    this.getUsers()
  }

  getUsers()
  {
    return this.UserService.requestDataUser().subscribe((response: any) => {
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

  AddUser(): void {
    const dialogRef = this.dialog.open(UserDialog, {
      data: {user: {}, callback: (user: User) =>
      {
        console.log('Add new User');
        this.UserService.addUser(user).subscribe((result)=>{
          this.getUsers()
        })
      }},
    });
  }

  DeleteUser(id: number): void {
    this.UserService.deleteUser(id).subscribe((result)=>{
      this.getUsers()
    })
  }

}
