import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { API_BASE_URL } from './../constants/http'
import { Observable, Subscriber } from 'rxjs';

import { Location } from 'src/models/location'

@Injectable({
  providedIn: 'root'
})
export class LocationService {


  constructor(private http: HttpClient) 
  {
  }

  requestData(): Observable<any>
  {
    return this.http.get(`${API_BASE_URL}/location`)
  }

  addLocation(user: Location): Observable<any>
  {
    return this.http.post(`${API_BASE_URL}/location`, user)
  }

  deleteLocation(id: number): Observable<any>
  {
    return this.http.delete(`${API_BASE_URL}/location/${id}`)
  }
}