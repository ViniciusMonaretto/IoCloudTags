import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginPageComponent } from 'src/panels/login-page/login-page.component';

import { MainScreenComponent } from 'src/panels/main-screen/main-screen.component';

const routes: Routes = [
  { path: 'login', component: LoginPageComponent }, // Define the route for MyComponent
  { path: 'main', component: MainScreenComponent }, // Define the route for MyComponent
  { path: '', redirectTo: '/login', pathMatch: 'full' } // Redirect to a default route
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
