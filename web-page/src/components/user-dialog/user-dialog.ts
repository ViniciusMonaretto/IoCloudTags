import { Component, Inject } from '@angular/core';
import {MAT_DIALOG_DATA, MatDialogRef} from '@angular/material/dialog';
import {UserTypes} from "../../enum/userTypes"
import {User} from "../../models/user"


@Component({
  selector: 'user-dialog',
  templateUrl: './user-dialog.html',
  styleUrls: ['./user-dialog.scss']
})
export class UserDialog {
  public userModule: User = new User("", "", "", 1, "", 0)

  public userTypes = Object.values(UserTypes);

  constructor(public dialogRef: MatDialogRef<UserDialog>,
    @Inject(MAT_DIALOG_DATA) public data: any
  ) {
    this.userModule = data.user
  }

  onNoClick(): void {
    this.dialogRef.close();
  }

  getUserData()
  {
    return {
      "Name": this.userModule.Name,
      "Email": this.userModule.Email,
      "PhoneNumber": this.userModule.PhoneNumber,
      "Type": this.userModule.Type,
      "Rfid": this.userModule.Rfid,
      "Password": this.userModule.Password
    }
  }

  validForm()
  {
    return this.userModule.Name != "" &&
           this.userModule.Email != "" &&
           this.userModule.PhoneNumber != "" &&
           this.userModule.Rfid != ""
  }

  onAddCLick(): void{
    this.data.callback(this.getUserData())
    this.dialogRef.close();
  }

}
