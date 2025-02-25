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

  public userTypes = Object.keys(UserTypes).filter(key => isNaN(Number(key)));;

  constructor(public dialogRef: MatDialogRef<UserDialog>,
    @Inject(MAT_DIALOG_DATA) public data: any
  ) {
    this.userModule = data.user
  }

  onNoClick(): void {
    this.dialogRef.close();
  }

  getRoleValue(roleName: any): number | undefined {
    return UserTypes[roleName as keyof typeof UserTypes]; // Lookup enum by key
  }

  getUserData()
  {
    return {
      "Name": this.userModule.Name,
      "Email": this.userModule.Email,
      "PhoneNumber": this.userModule.PhoneNumber,
      "Type": this.getRoleValue(this.userModule.Type),
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
