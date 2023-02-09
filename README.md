# ITCS 6166 Group Project

## Group Members

| Name | UNCC ID |
| --- | --- |
| Brian Borgia | 80039320 |
| Trevon Cornwell | 801213017 |
| David Gary | 801325583 |
| Lucky Kodwani | 801276339 |
| Joseph Mauney | 801008273 |

## Introduction

In this project we will be creating a web application to allow real-time video streaming between two users with the added ability to apply image filters to the video stream. Each user maintains a WebRTC connection to the host server, which will be responsible for relaying the video stream to the other user as well as applying the filters. The main filter we plan to implement utilizes the [CVPR2022-DaGAN model](https://github.com/harlanhong/CVPR2022-DaGAN) to detect the user's face and project a synthetically generated human face (either a celebrity or cartoon) in its place. The user will be able to select the face filter they want to apply. We hope to continue this project to include other, real-time filters, network performance optimizations, and mobile app extensions, but our main focus is a highly-performant, reliable, WebRTC video streaming application with the ability to apply a face filter using DaGAN.

## Architecture

This project will utilize a client-server architecture. Though any mobile app extensions we attempt as supplements will likely port their models to be run on the client-side, permitting any computation limitations. The client will be responsible for handling the user interface and its WebRTC connection to the server. The server will be responsible for receiving the initial video stream, running the DaGAN model, and relaying the modified stream to the other user. The server will also control the WebRTC signaling process.

## Biweekly Plan

| Date | Area of Focus | Product |
| --- | --- | --- |
| 02/13/2023 | Client-Server Architecture | Barebones client-server video streaming with WebRTC |
| 02/27/2023 | Mobile App Extensions and Model Deployment | A detailed internal team report on the feasibility of extra deployment options |
| 03/13/2023 | Model Deployment | Deploying the CVPR2022 DaGAN model in our application  |
| 03/27/2023 | System Testing | Complete testing of the system with detailed reports |
| 04/10/2023 | Refactoring and Refining | Refactoring and refining the codebase to maximize network performance |
| 04/24/2023 | Final Submission | Preparing presentations, documentation, and codebase for final submission |
