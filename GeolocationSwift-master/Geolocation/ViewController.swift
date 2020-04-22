//
//  ViewController.swift
//  Geolocation VERSION 1.4.6
//
//  Created by Eugene Tan on 2/12/20.
//  Copyright © 2020 Eugene Tan. All rights reserved.
//

import UIKit
import CoreLocation


class ViewController: UIViewController, CLLocationManagerDelegate {
    
    let locationManager = CLLocationManager()
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
        locationManager.requestAlwaysAuthorization()
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
        if let location = locations.first {
            //print(location.coordinate)
            //print(location.speed)
            
            //Added chunk here
            let dateFormatter = DateFormatter()
            dateFormatter.dateFormat = "MM-dd-yyyy HH:mm:ss"
            let dateInFormat = dateFormatter.string(from: Date())
            let deviceID = UIDevice.current.identifierForVendor!.uuidString
            
            //Added unique user ID
            
            //Changed the second : to string from double and added dateInFormat for string
            let parameters: [String : String] = ["User ID": deviceID, "Date": dateInFormat, "Longitude": String(location.coordinate.longitude), "Latitude": String(location.coordinate.latitude), "Speed": String(location.speed)]
            
            //let url = URL(string: "http://127.0.0.1:5000/post-requests")!
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
            
            //5 minute temporal sampling interval
            //sleep(300)
            
            task.resume()
            
            }
        }
    
    
    func locationManager(_ manager: CLLocationManager, didChangeAuthorization status: CLAuthorizationStatus) {
        if (status == CLAuthorizationStatus.denied) {
            showLocationDisabledPopUp()
        }
    }
    
    func showLocationDisabledPopUp() {
        let alertController = UIAlertController(title: "Background Location Access Disabled", message: "In order to find coordinates we need location.", preferredStyle: .alert)
        
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

