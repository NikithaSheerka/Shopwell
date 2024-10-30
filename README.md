# Shopwell - Nutri Label Scanner


## App to explain the food label
Develop a mobile app with camera support, the user points the camera on the food label on an item and the app provides an explanation on major ingredients and their benefits/problems. For example, if the label has the first ingredient as sugar, it warns the user. Some cryptic ingredients are explained in plain English.


> Problem Statement

1) Get Nutritional Informtaion from packaged foods Nutrition Labels and classify them as healhy or unhealthy

2) Explain the cryptic nutrients in label to the users with description

3) Visualize the nutrients quantity overall

4) Search for any food item to get the nutrients information in it


> Abstract

The concept of ”shop.well” stems from the notion that nutrition is essential to our diet. ”shop.well” is a smartphone application that scans the food label on packaged food products and generates major conclusions about the nutritional value any food brings to our diet, how many calories it delivers per serving, and which nutrients are present in that food. Our project utilizes Flutter as the front-end framework, which The concept of ”Shop well” stems from the notion that nutrition is essential to our diet. ”shop.well” is a smartphone application that scans the food label on packaged food products and generates major conclusions about the nutritional value any food brings to our diet, how many calories it delivers per serving, and which nutrients are present in that food.

> Approach

  • Planned and constructed the application while taking into account the necessary technology stack: Flutter, JavaScript runtime environment: Node.js, MongoDB, OpenCV, tesseract, Python, and Flask. <br>
  • Frontend (Flutter SDK) and backend development began simultaneously (both node server and ML server). <br>
  • Added user authentication and presented information based on the user’s input to personalize the program. <br>
  • Communicated between the frontend and the backend (Flutter with the node server and node with the flask server. <br>


> Persona 

Any User/Customers with a Smartphone who wants to get nutritional insights about packaged food.

> Architechure Diagram

![WhatsApp Image 2022-05-18 at 7 30 29 PM (1)](https://user-images.githubusercontent.com/25033517/169194861-2d6b0fa4-922a-4a0a-ad5c-eed4715dd28e.jpeg)

> Use Case Diagram

![WhatsApp Image 2022-05-18 at 7 30 29 PM](https://user-images.githubusercontent.com/25033517/169194691-1c3ede50-b20e-460d-bd57-9b6eb814de9b.jpeg)


> API Block Diagram

![WhatsApp Image 2022-05-18 at 7 30 29 PM (2)](https://user-images.githubusercontent.com/25033517/169194924-7bf9043c-72fc-4265-aa39-002de02e9330.jpeg)

> Run the Flutter App


```console

cd shopwell_app
flutter clean
flutter pub get
cd ios
pod install
flutter run

```

> Run the Backend


```console

cd api
npm install
node app.js

```


