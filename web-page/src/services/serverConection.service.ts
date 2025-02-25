import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';

import { API_BASE_URL } from './../constants/http'
import { Observable, Subscriber } from 'rxjs';

import { UserTypes } from 'src/enum/userTypes';

import { User } from 'src/models/user';
import { Location } from 'src/models/location';
import { MatDialog } from '@angular/material/dialog';
import { Router } from '@angular/router';
import { AlertDialogComponent } from 'src/components/alert-dialog/alert-dialog.component';

class UserInfo {
    public userId: number
    public userType: UserTypes

    constructor(userId: number, userType: UserTypes)
    {
        this.userId = userId
        this.userType = userType
    }
}

@Injectable({
  providedIn: 'root'
})
export class ServerConnectionService {

    userInfo: UserInfo | null = null

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

    getLoggedInInfo()
    {
        this.http.get(`${API_BASE_URL}/logout`).subscribe((result: any)=>{
            this.userInfo = new UserInfo(result.userId, result.userType)
        })
    }

    getEvents(idOfUser: any|null, idOfLocation: any|null): Observable<any>
    {
        let params = new HttpParams();
        if(idOfUser)
        {  
            params = params.append("Id", idOfUser);
        }

        if(idOfLocation)
        {
            params = params.append("LocaionId", idOfLocation);
        }
            
        
        
        return this.http.get(`${API_BASE_URL}/event`, { params })
    }

    addEvent(event: any)
    {
        return this.http.post(`${API_BASE_URL}/event`, event)
    }

    login(username: string, password: string) {
        const headers = new HttpHeaders().set('X-Skip-Error-Log', 'true');
        let body = { "username": username, "password": password }
        this.http.post(`${API_BASE_URL}/login`, body, { headers }).subscribe({
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

    hasAdminAccess()
    {
        return this.userInfo?.userType === UserTypes.Administrador
    }

    hasManagerAccess()
    {
        return this.hasAdminAccess() || this.userInfo?.userType === UserTypes.Sindico
    }
}