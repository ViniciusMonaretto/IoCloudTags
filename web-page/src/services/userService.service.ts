import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { API_BASE_URL } from './../constants/http'
import { Observable, Subscriber } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class UserService {


  constructor(private http: HttpClient) 
  {
  }

  requestData(): Observable<any>
  {
    return this.http.get(`${API_BASE_URL}/user`)
  }
}