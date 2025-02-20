import { Component, OnInit } from '@angular/core';
import { ServerConnectionService } from 'src/services/serverConection.service';

@Component({
  selector: 'app-login-page',
  templateUrl: './login-page.component.html',
  styleUrls: ['./login-page.component.scss']
})
export class LoginPageComponent implements OnInit {

  username = ""
  password = ""
  constructor(public LoginService: ServerConnectionService) { }

  ngOnInit(): void {
  }

  login()
  {
    this.LoginService.login(this.username, this.password)
  }

  validForm()
  {
    return this.username != "" && this.password != ""
  }

}
