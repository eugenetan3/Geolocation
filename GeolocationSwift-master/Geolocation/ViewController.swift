    //
//  ViewController.swift
//  Geolocation
//
//  Created by Eugene Tan on 2/12/20.
//  Copyright © 2020 Eugene Tan. All rights reserved.
//

import UIKit
import CoreLocation


//####
    
struct prevLocation {
    var latitude: Double = 0.00
    var longitude: Double = 0.00
    var time: Int = 0
    var CLItem : CLLocation = CLLocation(latitude: 0.00, longitude: 0.00)
    //var start: CFAbsoluteTime! = CFAbsoluteTimeGetCurrent()
    //var timecounter = NSDate()
}
var clock = prevLocation()

//####
//Find a starting point time, check if it is 5 minutes past that start time,
//if it is 5 minutes past that start time, assign that 5 min past time to a var inside struct
//then update timespent accordingly.

class ViewController: UIViewController, CLLocationManagerDelegate {
    
    
    let locationManager = CLLocationManager()
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
        
        //##ADDED CODE HERE
        
        locationManager.requestAlwaysAuthorization()
        
        let status = CLLocationManager.authorizationStatus()
        
        switch status {
            case .authorizedAlways:
                locationManager.startUpdatingLocation()
            case .authorizedWhenInUse:
                locationManager.requestAlwaysAuthorization()
                locationManager.startUpdatingLocation()
            case .restricted, .notDetermined:
                locationManager.requestAlwaysAuthorization()
            case .denied:
                showLocationDisabledPopUp()

        }
        
        //#####END ADDED CODE
        
        
        //locationManager.requestAlwaysAuthorization() this line can be uncommented
        // let deviceID = UIDevice.current.identifierForVendor?.uuidString
        //locationManager.requestWhenInUseAuthorization()
        
        if CLLocationManager.locationServicesEnabled() {
            locationManager.delegate = self
            locationManager.desiredAccuracy = kCLLocationAccuracyBest
            locationManager.startUpdatingLocation()
            locationManager.allowsBackgroundLocationUpdates = true
        }
    }
    

    func locationManager(_ manager: CLLocationManager, didUpdateLocations locations: [CLLocation]) {
        //
        
        if let location = locations.first {
            //###
            let maxTime:TimeInterval = 60*5;
            
            let locationIsValid:Bool = Date().timeIntervalSince(clock.CLItem.timestamp) >= maxTime
            print(locationIsValid)
            if locationIsValid {
                
            clock.CLItem = location
            //###
            //print(location.coordinate)
            //print(location.speed)
            //##
            //let elapsed = CFAbsoluteTimeGetCurrent() - clock.start
            //print(elapsed)
            
            //if (elapsed >= 300) {
            //##
            //    clock.start = CFAbsoluteTimeGetCurrent()
            //####added code
            if (clock.latitude == 0.00 && clock.longitude == 0.00) {
                clock.time = 0
                clock.latitude = location.coordinate.latitude
                clock.longitude = location.coordinate.longitude
                clock.CLItem = location
            } else {
                let meters = location.distance(from: clock.CLItem)
                if (meters >= 30.48) {
                    clock.time = 0
                } else {
                    clock.time += 5
                }
                clock.CLItem = location
            }
            
            
            let dateFormatter = DateFormatter()
            dateFormatter.dateFormat = "MM-dd-yyyy HH:mm:ss"
            let dateInFormat = dateFormatter.string(from: Date())
            let deviceID = UIDevice.current.identifierForVendor!.uuidString
            
            
            //Changed the second : to string from double and added dateInFormat for string
            let parameters: [String : String] = ["User ID": deviceID, "Date": dateInFormat, "Longitude": String(location.coordinate.longitude), "Latitude": String(location.coordinate.latitude), "Speed": String(location.speed), "Time Spent": String(clock.time)]
            //added time
  
            let url = URL(string: "https://eugenet.pythonanywhere.com/post-requests")!
            
            let session = URLSession.shared
            
            var request = URLRequest(url: url)
            request.httpMethod = "POST"
            
            do {
                request.httpBody = try JSONSerialization.data(withJSONObject: parameters, options: .prettyPrinted)
            } catch let error {
                print(error.localizedDescription)
            }
            request.addValue("application/json", forHTTPHeaderField: "Content-Type")
            request.addValue("application/json", forHTTPHeaderField: "Accept")
            
  
            let task = session.dataTask(with: request, completionHandler: { data, response, error in

                guard error == nil else {
                    return
                }

                guard let data = data else {
                    return
                }

                do {
                    //create json object from data
                    if let json = try JSONSerialization.jsonObject(with: data, options: .mutableContainers) as? [String: Any] {
                        print(json)
                        // handle json...
                    }

                } catch _ {
                   // print(error.localizedDescription)
                }
            })
            
            
            task.resume()
            }
        }
            //}
        }
    
    
    func locationManager(_ manager: CLLocationManager, didChangeAuthorization status: CLAuthorizationStatus) {
        if (status == CLAuthorizationStatus.denied) {
            showLocationDisabledPopUp()
        }
        //###ADDED CODE HERE
        if (status == CLAuthorizationStatus.authorizedWhenInUse) {
            showLocationDisabledPopUp()
        }
        if (status == CLAuthorizationStatus.notDetermined) {
            showLocationDisabledPopUp()
        }
        //###END ADDED CODE
    }
    
    func showLocationDisabledPopUp() {
        let alertController = UIAlertController(title: "Background Location Access Not Set to Always", message: "In order to find coordinates we need location.", preferredStyle: .alert)
        
        let cancelAction = UIAlertAction(title: "Cancel", style: .cancel, handler: nil)
        alertController.addAction(cancelAction)
        
        let openAction = UIAlertAction(title: "Open Settings", style: .default) { (action) in
            if let url = URL(string: UIApplication.openSettingsURLString) {
                UIApplication.shared.open(url, options: [:], completionHandler: nil)
            }
        }
        alertController.addAction(openAction)
        self.present(alertController, animated: true, completion: nil)
    }
}

