import { Component, OnInit } from '@angular/core';
import { Location } from 'src/models/location'
import { LocationService } from 'src/services/locationService.service';
import {MatDialog, MatDialogRef} from '@angular/material/dialog';
import { LocationDialog } from 'src/components/location-dialog/location-dialog';

@Component({
  selector: 'locations-page',
  templateUrl: './locations-page.component.html',
  styleUrls: ['./locations-page.component.scss']
})
export class LocationsPageComponent implements OnInit {

  locations: Array<Location> = []

  constructor( private locationService: LocationService,  private dialog: MatDialog) { }

  ngOnInit(): void {
    this.getLocations()
  }

  getLocations()
  {
    return this.locationService.requestData().subscribe((response: any) => {
      this.locations = []
      for(let locationInfo of response)
      {
        let info = locationInfo.replace(/'/g, '"')
        info = info.replace('None' , "null")
        info = JSON.parse(info)
        this.locations.push(new Location(info["Name"], info["Block"], info["Sector"], info["GatewayUuid"], info["AdminUserId"], info["Id"]))
      }
    })
  }

  AddLocation(): void {
    const dialogRef = this.dialog.open(LocationDialog, {
      data: {user: {}, callback: (location: Location) =>
      {
        console.log('Add Location');
        this.locationService.addLocation(location).subscribe((result)=>{
          this.getLocations()
        })
      }},
    });
  }

  DeleteLocation(id: number): void {
    this.locationService.deleteLocation(id).subscribe((result)=>{
      this.getLocations()
    })
  }

}
