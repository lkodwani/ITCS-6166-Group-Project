# Plan Updates for Final Project

For tonight's iteration update push, we are instead providing a report on where we are, the challenges faced, and the ideas we have for the future. After seeing other presentations during Monday's lecture, it is clear that the fact that we have functional, two-way video streaming, a proper signaling server, and our model image overlay implemented puts us further along than many other groups. Still, this does not mean the direction going forward makes sense, so we are going to reevaluate and quickly rework our plan.

## Current Issues

### Model Deployment

Initially, we planned to cartoonify or add a synthesized overlay image to user faces in a video stream using the [CVPR2022-DaGAN model](https://github.com/harlanhong/CVPR2022-DaGAN), and while we have been able to make this work locally on video streams, there is a significant delay as it requires the video stream to be saved to a file, processed, and then reloaded. This is not a viable solution for a "real-time" application, and it heavily relies on the use of the signaling server to perform these. If the main goal of using WebRTC is to outsource much of the work into a P2P network between clients, why redirect a bulk of the work back to a server? We want to avoid heavy communication cost, and this is simply not the right way to go about it.

### Reinforcement Learning Based Optimization

We have exhaustively reviewed the current literature on reinforcement learning based approaches to optimizing network performance, only to find roadblocks and clear dead-ends. The existing OpenNetLab works seem to be the most recent and promising direction, but these are (almost entirely) for large scale enterprise networks. Our application is a simple, video streaming chatroom. Optimization decisions made by an RL agent, even a pretrained one (though this is not a simple deployment process either), would be overkill and almost certainly unsuccessful. We have metric collection processes programmed out, and there is hope to construct a policy around these, but this will involve training an RL agent from scratch. We will discuss this matter with the TA tomorrow.

## Next Steps

Outside of discussing the matters with the TA and Dr. Wang over the next two days, we are preparing to follow the flow of the rest of the class if we are unable to devise appropriate solutions before Saturday. But, as a team, we feel that heavily relying on Streamlit to handle the majority of the difficult processes is not the most educational or beneficial method. So we are also considering using the javascript implementation of OpenCV to perform the image processing and image overlay on the client-side, which would allow the P2P architecture to be preserved and the signaling server to be used only for signaling. We will see if this is a viable path in Ezra's eyes as well.

There is also a possibility that we revive our initial plan for implementing a P2P architecture from scratch, mostly designed around the Chord DHT model. Integrating WebRTC as the communication protocol between nodes in the ring, and allowing for the signaling server to help manage the creation, entry, and exiting of nodes from the ring would capture the spirit of deeply learning the WebRTC protocol, but this would be lacking in the ML aspect of the project. We will discuss this matter as well tomorrow.
