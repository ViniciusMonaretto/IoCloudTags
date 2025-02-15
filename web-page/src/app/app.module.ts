import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms'; // Import FormsModule

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HttpClientModule } from '@angular/common/http';

import { MainScreenComponent } from 'src/panels/main-screen/main-screen.component';
import { NavbarComponent } from 'src/panels/navbar/navbar.component';
import { UserPageComponent } from 'src/panels/user-page/user-page.component'
import { LocationsPageComponent } from 'src/panels/locations-page/locations-page.component'


//selfmade components
import { SideNavOptionComponent } from 'src/components/side-nav-option/side-nav-option.component';
import { IoCloudTableComponent } from 'src/components/io-cloud-table/io-cloud-table.component'
import { UserDialog } from 'src/components/user-dialog/user-dialog'
import { LocationDialog } from 'src/components/location-dialog/location-dialog'


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


@NgModule({
  declarations: [
    AppComponent,
    MainScreenComponent,
    NavbarComponent,
    UserPageComponent,
    LocationsPageComponent,

    SideNavOptionComponent,
    IoCloudTableComponent,
    UserDialog,
    LocationDialog
  ],
  imports: [
    BrowserModule,
    FormsModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    HttpClientModule,

    MatSidenavModule,
    MatToolbarModule,
    MatIconModule,
    MatButtonModule,
    MatDialogModule,
    MatFormFieldModule,
    MatSelectModule,
    MatInputModule,
    MatCardModule,
    MatTableModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
