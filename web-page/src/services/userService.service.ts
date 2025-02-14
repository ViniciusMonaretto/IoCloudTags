import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { API_BASE_URL } from './../constants/http'
import { Observable, Subscriber } from 'rxjs';

import { User } from 'src/models/user';

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

  addUser(user: User): Observable<any>
  {
    return this.http.post(`${API_BASE_URL}/user`, user)
  }

  deleteUser(id: number): Observable<any>
  {
    return this.http.delete(`${API_BASE_URL}/user/${id}`)
  }
}