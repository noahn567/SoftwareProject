import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SharedService {
readonly APIUrl = "http://127.0.0.1:8000"

  constructor(private http:HttpClient) {}

  getSubscriptionList():Observable<any[]>{
    return this.http.get<any[]>(this.APIUrl + '/subscription/')
  }

  addSubscription(val:any){
    return this.http.post(this.APIUrl + '/subscription/',val)
  }

  subscriptionSendUpdate(val:any){
    return this.http.post(this.APIUrl + '/subscription/sendupdate',val)
  }

  updateSubscription(val:any){
    return this.http.put(this.APIUrl + '/subscription/',val)
  }

  deleteSubscription(val:any){
    return this.http.delete(this.APIUrl + '/subscription/'+val)
  }

  getAllSubscriptionNames():Observable<any[]>{
    return this.http.get<any[]>(this.APIUrl+'/subscription/');
  }
}
