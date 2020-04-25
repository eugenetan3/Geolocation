//
//  ViewController.swift
//  Geolocation
//
//  Created by Eugene Tan on 2/12/20.
//  Copyright © 2020 Eugene Tan. All rights reserved.
//

import UIKit
import CoreLocation

//Global struct used to hold previous CLLocation Object
struct prevLocation {
    var latitude: Double = 0.00
    var longitude: Double = 0.00
    var time: Int = 0
    var CLItem : CLLocation = CLLocation(latitude: 0.00, longitude: 0.00)
}
var clock = prevLocation()


//Find a starting point time, check if it is 5 minutes past that start time,
//if it is 5 minutes past that start time, assign that 5 mintime to a var inside struct
//then update timespent accordingly.

class ViewController: UIViewController, CLLocationManagerDelegate {
    
    
    let locationManager = CLLocationManager()
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
        
        //Request user for location access even in the background
        locationManager.requestAlwaysAuthorization()
        
        //Check user status
        let status = CLLocationManager.authorizationStatus()
        
        //Evaluate which case, until user has provided access to always allowing location tracking
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
        
        //Check if the user has enabled location services, if true we assign accuracy and begin updating
        if CLLocationManager.locationServicesEnabled() {
            locationManager.delegate = self
            locationManager.desiredAccuracy = kCLLocationAccuracyBest
            locationManager.startUpdatingLocation()
            locationManager.allowsBackgroundLocationUpdates = true //Allows app to run in background due to build capability
        }
    }
    

    func locationManager(_ manager: CLLocationManager, didUpdateLocations locations: [CLLocation]) {
        
        //Get the first location within locations
        if let location = locations.first {
            
            let maxTime:TimeInterval = 60*5; //Temporal Sampling Interval of 5 minutes
            
            //Check to see if it has been 5 minutes since the last item has been updated (CL.item within clock struct)
            let locationIsValid:Bool = Date().timeIntervalSince(clock.CLItem.timestamp) >= maxTime
            // Debug statement: print(locationIsValid)
            if locationIsValid { //5 minutes has passed so we continue and parse and send a new location to web server
                
            clock.CLItem = location //Update location within the struct so it becomes the "previous" location
          
            if (clock.latitude == 0.00 && clock.longitude == 0.00) { //If a location has not been encountered before we assign defaults to struct
                clock.time = 0 //Time spent in one location
                clock.latitude = location.coordinate.latitude //Assign lat
                clock.longitude = location.coordinate.longitude //Assign long
                clock.CLItem = location //Assign CLLocation object
            } else {
                let meters = location.distance(from: clock.CLItem) //Check how far away from previous location the current location is
                if (meters >= 30.48) { //If location is >100ft away from previous location, reset timespent (movement)
                    clock.time = 0
                } else {
                    clock.time += 5 //Increment time spent if location within 100ft from previous location
                }
                clock.CLItem = location //Assign location update
            }
            
            
            let dateFormatter = DateFormatter()
            dateFormatter.dateFormat = "MM-dd-yyyy HH:mm:ss"
            let dateInFormat = dateFormatter.string(from: Date()) //Format time stamp so that it follows dateFormatter (MM-dd-yyyy HH:mm:ss)
            let deviceID = UIDevice.current.identifierForVendor!.uuidString //Get a unique user id that is assigned to a user's device upon installation
            
            
            //JSON package format (dictionary)
            let parameters: [String : String] = ["User ID": deviceID, "Date": dateInFormat, "Longitude": String(location.coordinate.longitude), "Latitude": String(location.coordinate.latitude), "Speed": String(location.speed), "Time Spent": String(clock.time)]
            
            //URL to send the parameters JSON to the web server where the data is sent to
            let url = URL(string: "https://eugenet.pythonanywhere.com/post-requests")!
            
            let session = URLSession.shared
            
            var request = URLRequest(url: url)
            request.httpMethod = "POST" //https POST request
            
            do {
                request.httpBody = try JSONSerialization.data(withJSONObject: parameters, options: .prettyPrinted)
            } catch let error {
                print(error.localizedDescription)
            }
            request.addValue("application/json", forHTTPHeaderField: "Content-Type")
            request.addValue("application/json", forHTTPHeaderField: "Accept")
            //JSON serialization to make JSON from parameters 
            
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
   
        }
    
    
    func locationManager(_ manager: CLLocationManager, didChangeAuthorization status: CLAuthorizationStatus) {
        if (status == CLAuthorizationStatus.denied) { 
            showLocationDisabledPopUp() //Popup 
        }
   
        if (status == CLAuthorizationStatus.authorizedWhenInUse) {
            showLocationDisabledPopUp() //Popup
        }
        if (status == CLAuthorizationStatus.notDetermined) {
            showLocationDisabledPopUp() //Popup
        }
 
    }
    
    //UI controller which gives phone prompt alert
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

