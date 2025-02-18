import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'io-cloud-table',
  templateUrl: './io-cloud-table.component.html',
  styleUrls: ['./io-cloud-table.component.scss']
})
export class IoCloudTableComponent implements OnInit {

  @Input() models: any[] = [];
  @Input() headerInfo: string[][] = [];
  @Input() title: string = "";
  @Output() editCallback: EventEmitter<any> = new EventEmitter();
  @Output() deleteCallback: EventEmitter<any> = new EventEmitter();
  @Output() addCallback: EventEmitter<any> = new EventEmitter();

  constructor() { }

  ngOnInit(): void {
  }

  getModelInfo(key: string, model: any)
  {
    return model[key]
  }

  onDeleteCallback(id:number)
  {
    let result = confirm("Are you sure you want to delete the user?");
    if (result === true) {

      this.deleteCallback.emit(id)
    } 
    
  }

}
