import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'io-cloud-table',
  templateUrl: './io-cloud-table.component.html',
  styleUrls: ['./io-cloud-table.component.scss']
})
export class IoCloudTableComponent implements OnInit {

  @Input() models: any[] = [];
  @Input() headerInfo: string[] = [];
  @Output() buttonCallback: EventEmitter<any> = new EventEmitter();

  constructor() { }

  ngOnInit(): void {
  }

  getModelInfo(key: string, model: any)
  {
    return model[key]
  }

}
