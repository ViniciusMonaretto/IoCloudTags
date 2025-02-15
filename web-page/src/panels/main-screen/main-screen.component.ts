import { Component, OnInit } from '@angular/core';
import { MainScreenService } from 'src/services/mainScreenService.service'

@Component({
  selector: 'app-main-screen',
  templateUrl: './main-screen.component.html',
  styleUrls: ['./main-screen.component.scss']
})
export class MainScreenComponent implements OnInit {

  constructor(public mainScreenService: MainScreenService) { }

  ngOnInit(): void {
  }

}
