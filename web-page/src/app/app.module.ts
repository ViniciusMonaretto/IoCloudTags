import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms'; // Import FormsModule

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HTTP_INTERCEPTORS, HttpClientModule } from '@angular/common/http';

import { MainScreenComponent } from 'src/panels/main-screen/main-screen.component';
import { NavbarComponent } from 'src/panels/navbar/navbar.component';
import { UserPageComponent } from 'src/panels/user-page/user-page.component'
import { LocationsPageComponent } from 'src/panels/locations-page/locations-page.component'
import { LoginPageComponent } from 'src/panels/login-page/login-page.component';
import { ScheduleCalendarComponent } from 'src/panels/schedule-calendar/schedule-calendar.component';


//selfmade components
import { SideNavOptionComponent } from 'src/components/side-nav-option/side-nav-option.component';
import { IoCloudTableComponent } from 'src/components/io-cloud-table/io-cloud-table.component'
import { UserDialog } from 'src/components/user-dialog/user-dialog'
import { LocationDialog } from 'src/components/location-dialog/location-dialog'
import { AlertDialogComponent } from 'src/components/alert-dialog/alert-dialog.component';
import { EventDialogComponent } from 'src/components/event-dialog/event-dialog.component';



//Angular Material
import {MatSidenavModule} from '@angular/material/sidenav';
import {MatToolbarModule} from '@angular/material/toolbar';
import {MatIconModule} from '@angular/material/icon';
import {MatButtonModule} from '@angular/material/button'; 
import {MatDialogModule} from '@angular/material/dialog'; 
import {MatFormFieldModule} from '@angular/material/form-field'; 
import {MatSelectModule } from '@angular/material/select'; 
import {MatInputModule } from '@angular/material/input'; 
import {MatCardModule} from '@angular/material/card'; 
import {MatTableModule} from '@angular/material/table'; 
import { AuthInterceptor } from 'src/services/auth.interceptor';
import { FullCalendarModule } from '@fullcalendar/angular';
import { MatNativeDateModule } from '@angular/material/core';
import { MatDatepickerModule } from '@angular/material/datepicker';


@NgModule({
  declarations: [
    AppComponent,
    MainScreenComponent,
    NavbarComponent,
    UserPageComponent,
    LocationsPageComponent,
    LoginPageComponent,
    ScheduleCalendarComponent,

    SideNavOptionComponent,
    IoCloudTableComponent,
    UserDialog,
    LocationDialog,
    AlertDialogComponent,
    EventDialogComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    HttpClientModule,
    FullCalendarModule,

    MatSidenavModule,
    MatToolbarModule,
    MatIconModule,
    MatButtonModule,
    MatDialogModule,
    MatFormFieldModule,
    MatSelectModule,
    MatInputModule,
    MatDatepickerModule,
    MatNativeDateModule,
    MatCardModule,
    MatTableModule
  ],
  providers: [{
    provide: HTTP_INTERCEPTORS,
    useClass: AuthInterceptor,
    multi: true
  }],
  bootstrap: [AppComponent]
})
export class AppModule { }
