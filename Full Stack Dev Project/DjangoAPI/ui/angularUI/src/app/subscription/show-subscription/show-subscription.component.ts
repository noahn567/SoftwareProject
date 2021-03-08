import { Component, OnInit } from '@angular/core';
import { SharedService } from 'src/app/shared.service';


@Component({
  selector: 'app-show-subscription',
  templateUrl: './show-subscription.component.html',
  styleUrls: ['./show-subscription.component.css']
})
export class ShowSubscriptionComponent implements OnInit {

  constructor(private service:SharedService) { }

  SubscriptionList:any=[];
  subscription:any;

  // Add Subscription
  addSubscription(newSubscriptionStockTicker: string,newSubscriptionContactNumber: string) {
    if (newSubscriptionStockTicker && newSubscriptionContactNumber) {
      var val = {SubscriptionStockTicker:newSubscriptionStockTicker,SubscriptionContactNumber:newSubscriptionContactNumber};
      this.service.addSubscription(val).subscribe(res=>{
        if(res.toString().includes("Error:")) alert(res.toString());
        this.refreshSubscriptionList();
      });
    }
  }

  // Get Subscription list on Start
  ngOnInit(): void {
    this.refreshSubscriptionList();
  }

  // Manual Send Update to Subscription
  SendUpdate(subscription) {
    if (subscription) {
      this.service.subscriptionSendUpdate(subscription).subscribe(res=>{
        this.refreshSubscriptionList();
      });
    }
  }

  // Delete Subsciption
  deleteSubscription(item){
    this.subscription=item;
    var val = this.subscription.SubscriptionId;
      this.service.deleteSubscription(val).subscribe(res=>{
        this.refreshSubscriptionList();
      });
  }

  // Refresh Subscriptions
  refreshSubscriptionList(){
    this.service.getSubscriptionList().subscribe(data=>{
      this.SubscriptionList=data;
    });
  }
  
}
