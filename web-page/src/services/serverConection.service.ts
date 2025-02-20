import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { API_BASE_URL } from './../constants/http'
import { Observable, Subscriber } from 'rxjs';

import { User } from 'src/models/user';
import { Location } from 'src/models/location';
import { MatDialog } from '@angular/material/dialog';
import { Router } from '@angular/router';
import { AlertDialogComponent } from 'src/components/alert-dialog/alert-dialog.component';

@Injectable({
  providedIn: 'root'
})
export class ServerConnectionService {

    constructor(private http: HttpClient, private dialog: MatDialog, private router: Router) 
    {
    }

    requestDataUser(): Observable<any>
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

    requestDataLocation(): Observable<any>
    {
        return this.http.get(`${API_BASE_URL}/location`)
    }

    addLocation(location: Location): Observable<any>
    {
        return this.http.post(`${API_BASE_URL}/location`, location)
    }

    deleteLocation(id: number): Observable<any>
    {
        return this.http.delete(`${API_BASE_URL}/location/${id}`)
    }

    login(username: string, password: string) {
        let body = { "username": username, "password": password }
        this.http.post(`${API_BASE_URL}/login`, body).subscribe({
        next: (result: any) => {
            localStorage.setItem('auth_token', result.token);
            this.router.navigate(['/main'])

        },
        error: (result) => {
            this.dialog.open(AlertDialogComponent, {
            width: '300px',
            data: { message: "Usuário ou Senha errados" }
            })
        }
        })
    }
}