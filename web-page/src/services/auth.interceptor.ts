import { Injectable } from '@angular/core';
import { HttpRequest, HttpHandler, HttpEvent, HttpInterceptor, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { Router } from '@angular/router';
import { AlertDialogComponent } from 'src/components/alert-dialog/alert-dialog.component';
import { MatDialog } from '@angular/material/dialog';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  [x: string]: any;
  constructor(private router: Router, private dialog: MatDialog) {}


  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {

    const token = localStorage.getItem('auth_token');
    
    if (token) {
      request = request.clone({
        setHeaders: {
          'Content-Type' : 'application/json; charset=utf-8',
          'Accept'       : 'application/json',
          'Authorization': token
        }
      });
    }

    return next.handle(request).pipe(
      catchError((error: HttpErrorResponse) => {
        const skipErrorLog = request.headers.get('X-Skip-Error-Log') === 'true';
        if (!skipErrorLog) {
          this.logError(error); // Log error if the flag is not present
        }
        if (error.status === 401) {
          this.router.navigate(['/login']);
        }
        return throwError(() => error);
      })
    );
  }

  private logError(error: HttpErrorResponse): void {
    // Log the error to the console
    this.dialog.open(AlertDialogComponent, {
      width: '300px',
      data: { message: error.message }
      })
  }

}
