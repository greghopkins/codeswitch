import { Component, OnInit } from '@angular/core';
import { Validators, FormGroup, FormControl } from '@angular/forms';
import { Router } from '@angular/router';
import { MenuController } from '@ionic/angular';

import { environment } from '../../environments/environment';

import { UserPasswordCredential } from 'mongodb-stitch-browser-sdk';

@Component({
  selector: 'app-login',
  templateUrl: './login.page.html',
  styleUrls: ['./styles/login.page.scss']
})
export class LoginPage implements OnInit {
  loginForm: FormGroup;

  constructor(public router: Router, public menu: MenuController) {
    this.loginForm = new FormGroup({
      email: new FormControl('greg.hopkins+u1@gmail.com'),
      password: new FormControl('Test@123')
    });
  }

  ngOnInit(): void {
    this.menu.enable(false);
  }

  doLogin(): void {
    const credential = new UserPasswordCredential(
      this.loginForm.value.email,
      this.loginForm.value.password
    );

    environment.stitchClient.auth
      .loginWithCredential(credential)
      .then(authedUser =>
        console.log(`successfully logged in with id: ${authedUser.id}`)
      )
      .catch(err => console.error(`login failed with error: ${err}`));
    this.router.navigate(['/getting-started']);
  }
}
