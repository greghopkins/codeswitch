import {
  Component,
  OnInit,
  AfterViewInit,
  ViewChild,
  HostBinding
} from '@angular/core';
import { FormGroup, FormControl, FormArray } from '@angular/forms';

import { IonSlides, MenuController } from '@ionic/angular';

import { environment } from '../../environments/environment';

import { RemoteMongoClient } from 'mongodb-stitch-browser-sdk';

@Component({
  selector: 'app-getting-started',
  templateUrl: './getting-started.page.html',
  styleUrls: [
    './styles/getting-started.page.scss',
    './styles/getting-started.shell.scss',
    './styles/getting-started.responsive.scss'
  ]
})
export class GettingStartedPage implements OnInit, AfterViewInit {
  @ViewChild(IonSlides) slides: IonSlides;
  @HostBinding('class.last-slide-active') isLastSlide = false;

  gettingStartedForm: FormGroup;

  services: Array<any>;

  constructor(public menu: MenuController) {
    this.gettingStartedForm = new FormGroup({
      interestedServices: new FormArray([])
    });
  }

  ngOnInit(): void {
    this.menu.enable(false);

    const mongodb = environment.stitchClient.getServiceClient(
      RemoteMongoClient.factory,
      'codeswitch'
    );

    const services = mongodb.db('default').collection('services');
    services
      .find({})
      .asArray()
      .then(_ => {
        this.services = _;
        this.services.map((o, i) => {
          const control = new FormControl(false);
          (this.gettingStartedForm.controls
            .interestedServices as FormArray).push(control);
        });
      });
  }

  ngAfterViewInit(): void {
    // ViewChild is set
    this.slides.isEnd().then(isEnd => {
      this.isLastSlide = isEnd;
    });

    // Subscribe to changes
    this.slides.ionSlideWillChange.subscribe(changes => {
      this.slides.isEnd().then(isEnd => {
        this.isLastSlide = isEnd;
      });
    });
  }
}
