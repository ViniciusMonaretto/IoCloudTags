import { Component, OnInit } from '@angular/core';
import {MatDialog} from '@angular/material/dialog';

import { MainScreenService } from 'src/services/mainScreenService.service'
import { ServerConnectionService } from 'src/services/serverConection.service';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss']
})
export class NavbarComponent implements OnInit {

  constructor(public dialog: MatDialog, public mainScreenService: MainScreenService, 
    public serverConnection: ServerConnectionService) { }

  ngOnInit(): void {
    this.serverConnection.getLoggedInInfo()
  }

  selectMainScreen(screen: string)
  {
    this.mainScreenService.setScreenType(screen)
  }

}
