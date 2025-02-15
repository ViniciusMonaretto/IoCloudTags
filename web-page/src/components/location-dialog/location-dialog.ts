import { Component, Inject } from '@angular/core';
import {MAT_DIALOG_DATA, MatDialogRef} from '@angular/material/dialog';
import {UserTypes} from "../../enum/userTypes"
import {Location} from "../../models/location"


@Component({
  selector: 'user-dialog',
  templateUrl: './location-dialog.html',
  styleUrls: ['./location-dialog.scss']
})
export class LocationDialog {
  public locationModel: Location = new Location("", 0, 0, "", 1,  0)

  constructor(public dialogRef: MatDialogRef<LocationDialog>,
    @Inject(MAT_DIALOG_DATA) public data: any
  ) {
    this.locationModel = data.user
  }

  onNoClick(): void {
    this.dialogRef.close();
  }

  getLocationData()
  {
    return {
      "Name": this.locationModel.Name,
      "Block": this.locationModel.Block,
      "Sector": this.locationModel.Sector,
      "Uuid": this.locationModel.GatewayUUID,
      "AdminUserId": this.locationModel.ManagerId,
      "Id": this.locationModel.Id
    }
  }

  validForm()
  {
    return this.locationModel.ManagerId != 0 &&
           this.locationModel.GatewayUUID != "" 
  }

  onAddCLick(): void{
    this.data.callback(this.getLocationData())
    this.dialogRef.close();
  }

}
