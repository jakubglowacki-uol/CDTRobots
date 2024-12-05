import cv2

import numpy as np
 
import matplotlib.pyplot as plt

import csv

class ViscosityClassifier:
    def __init__(self):
        self.model = ""
        self.motion_delay = 0.3
        self.white_threshold = 129

    # return true if viscous, false if not
    def classifyVideo(self, video_path: str):
        cap = cv2.VideoCapture(video_path)

        # Check if the video file was successfully opened
        if not cap.isOpened():
            print("Error: Could not open the video.")
        else:
            print('file opened')

        # Get the video's properties like frame width, height, fps
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # Set the clipping parameters (e.g., clip from 10s to 20s)
        start_time = 20  # start time in seconds
        end_time = 53    # end time in seconds

        # Set the start and end frames for the clip
        start_frame = int(start_time * fps)
        end_frame = int(end_time * fps)

        # Define the cropping area (x, y, width, height)
        x, y, w, h = 80, 120, 340, 150  # Crop a region starting at (x, y) with width w and height h
        print("before video opening")
        # Define the codec and create a VideoWriter object to save the output
        fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Codec for .mp4
        out = cv2.VideoWriter('output_video.avi', fourcc, fps, (w, h))  # Output size is cropped size
        print("video after output creation")
        # Set the starting frame position to clip the video
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

        frame_num = start_frame
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("failure writing")
                break
            print("got frame")
            # Check if we've reached the end frame
            if frame_num > end_frame:
                break

            # Crop the frame (ROI)
            cropped_frame = frame[y:y+h, x:x+w]
            print("cropped frame")
            # Write the cropped frame to the output video file
            out.write(cropped_frame)
            print("written cropped frame")
            # Increment the frame number
            frame_num += 1

            # Optional: Display the cropped frame (for debugging purposes)
            #cv2.imshow('Cropped Frame', cropped_frame)
            #if cv2.waitKey(1) & 0xFF == ord('q'):
            #   break

        # Release everything once job is done
        cap.release()
        out.release()
        cv2.destroyAllWindows()
            


        # we need to automate the video processing by making this a function/class 

        #------------------ invert

        # Open the video file

        cap = cv2.VideoCapture('output_video.avi')

        # Check if the video was opened successfully
        if not cap.isOpened():
            print("Error: Could not open video.")
        

        # Get the video properties (frame width, height, frames per second)
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)

        # Create a VideoWriter object to save the resulting video
        fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Codec for .avi format
        out = cv2.VideoWriter('video_inverted.avi', fourcc, fps, (frame_width, frame_height))

        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                break

            # Invert the colors by subtracting each pixel from 255
            inverted_frame = cv2.bitwise_not(frame)

            # Write the inverted frame to the output video
            out.write(inverted_frame)

        # Release the video capture and writer objects
        cap.release()
        out.release()
        cv2.destroyAllWindows()

        print("Color-inverted video saved successfully.")

        # Open the background and foreground video files
        bg_cap = cv2.VideoCapture('output_video.avi')
        fg_cap = cv2.VideoCapture('video_inverted.avi')

        # Check if the videos are opened successfully
        if not bg_cap.isOpened() or not fg_cap.isOpened():
            print("Error: Could not open one or both videos.")
        

        # Get properties of the background video
        bg_frame_width = int(bg_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        bg_frame_height = int(bg_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        bg_fps = bg_cap.get(cv2.CAP_PROP_FPS)

        # Get properties of the foreground video
        fg_fps = fg_cap.get(cv2.CAP_PROP_FPS)

        # Create a VideoWriter object to save the resulting video
        fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Codec for .mp4 format
        out = cv2.VideoWriter('output_video_with_opacity_and_delay.avi', fourcc, bg_fps, (bg_frame_width, bg_frame_height))

        # Define the delay (in frames) for the foreground video (2 seconds delay)
        delay_frames = int(bg_fps * self.motion_delay)  # 2 seconds delay, adjust as needed

        # Read frames from the background and foreground videos
        bg_frames = []
        fg_frames = []

        while bg_cap.isOpened() and fg_cap.isOpened():
            ret_bg, bg_frame = bg_cap.read()
            ret_fg, fg_frame = fg_cap.read()

            if not ret_bg or not ret_fg:
                break

            bg_frames.append(bg_frame)
            fg_frames.append(fg_frame)

        # Release the video capture objects
        bg_cap.release()
        fg_cap.release()

        # Now, overlay the frames with the desired delay and 50% opacity
        for i in range(len(bg_frames)):
            # Background frame
            bg_frame = bg_frames[i]

            # Foreground frame with delay
            if i - delay_frames >= 0:
                fg_frame = fg_frames[i - delay_frames]
            else:
                fg_frame = np.zeros_like(bg_frame)  # If the delay goes past the start, make the frame black

            # Resize the foreground to fit the background (if necessary)
            fg_resized = cv2.resize(fg_frame, (bg_frame_width, bg_frame_height))

            # Apply 50% opacity to both background and foreground using addWeighted
            overlay_frame = cv2.addWeighted(bg_frame, 0.5, fg_resized, 0.5, 0)  # 50% opacity for both

            # Write the resulting frame to the output video
            out.write(overlay_frame)

        # Release the output video writer
        out.release()

        print("Video with opacity and delay saved successfully.")

        # Open the input video
        cap = cv2.VideoCapture('output_video_with_opacity_and_delay.avi')

        # Check if the video was opened successfully
        if not cap.isOpened():
            print("Error: Could not open video.")
            
        # Get the video properties (frame width, height, frames per second)
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)

        # Create a VideoWriter object to save the resulting video
        fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Codec for .mp4 format
        out = cv2.VideoWriter('motion_video.avi', fourcc, fps, (frame_width, frame_height), False)

        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                break

            # Convert the frame to grayscale
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Threshold to turn midtones (greys) into black and amplify the whites
            # Any pixel value above 100 will remain as is, and others will be set to 0 (black)
            _, thresholded_frame = cv2.threshold(gray_frame, self.white_threshold, 255, cv2.THRESH_BINARY)

            # Amplify the whites: enhance the brightest pixels even more
            amplified_frame = cv2.convertScaleAbs(thresholded_frame, alpha=1.5, beta=0)

            # Write the processed frame to the output video
            out.write(amplified_frame)

        # Release the video capture and writer objects
        out.release()
        cv2.destroyAllWindows()

        print("motion video saved successfully.")
        
        
        #----------------------------------------------------------------------------------
        # Open the input video
        cap = cv2.VideoCapture('motion_video.avi')

        # Check if the video was opened successfully
        if not cap.isOpened():
            print("Error: Could not open video.")

        # Create lists to store frame counts and white pixel counts
        frame_counts1 = []
        white_pixel_counts1 = []
        cumulative_white_pixel_counts1 = []

        # Initialize variables to track the state
        frame_count1 = 0
        last_cumulative_count1 = 0
        unchanged_frame_count1 = 0

        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                break

            # Increment frame count
            frame_count1 += 1

            # Count the number of white pixels
            white_pixel_count1 = np.sum(frame == 255)

            # Calculate the cumulative sum of white pixel counts
            if len(cumulative_white_pixel_counts1) == 0:
                cumulative_sum1 = white_pixel_count1
            else:
                cumulative_sum1 = cumulative_white_pixel_counts1[-1] + white_pixel_count1

            # Check if the cumulative sum is unchanged for 10 frames
            if cumulative_sum1 == last_cumulative_count1:
                unchanged_frame_count1 += 1
            else:
                unchanged_frame_count1 = 0

            # Append the cumulative sum if it's stable, otherwise, continue appending the same value
            if unchanged_frame_count1 >=20:
                cumulative_white_pixel_counts1.append(last_cumulative_count1)  # Append previous cumulative value
                #print(cumulative_white_pixel_counts1)
                break
            else:
                cumulative_white_pixel_counts1.append(cumulative_sum1)  # Append the current cumulative sum

            # Update the last cumulative value
            last_cumulative_count1 = cumulative_sum1

            # Store the frame count (always append frame count)
            frame_counts1.append(frame_count1)

            # Optionally, append the pixel counts (if you need it for later processing)
            white_pixel_counts1.append(white_pixel_count1)

        # Calculate the cumulative sum of white pixel counts
        cumulative_white_pixel_counts1 = np.cumsum(white_pixel_counts1)

        # Find the index of the maximum cumulative white pixel count
        max_index = np.argmax(cumulative_white_pixel_counts1)

        # Find the corresponding frame count at the maximum cumulative white pixel count
        frame_at_max = frame_counts1[max_index]

        # Create lists to store frame counts and white pixel counts
        frame_counts2 = []
        white_pixel_counts2 = []
        cumulative_white_pixel_counts2 = []

        # Initialize variables to track the state
        frame_count2 = 0
        last_cumulative_count2 = 0
        unchanged_frame_count2 = 0

        cap = cv2.VideoCapture('motion_video.avi')

        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                break

            # Increment frame count
            frame_count2 += 1

            # Count the number of white pixels
            white_pixel_count2 = np.sum(frame == 255)

            # Calculate the cumulative sum of white pixel counts
            if len(cumulative_white_pixel_counts2) == 0:
                cumulative_sum2 = white_pixel_count2
            else:
                cumulative_sum2 = cumulative_white_pixel_counts2[-1] + white_pixel_count2

            # Update the last cumulative value
            last_cumulative_count2 = cumulative_sum2

            # Store the frame count (always append frame count)
            frame_counts2.append(frame_count2)

            # Optionally, append the pixel counts (if you need it for later processing)
            white_pixel_counts2.append(white_pixel_count2)

        # Release the video capture object
        cap.release()

        #-------------------------------------------------

        # Print the maximum cumulative white pixel count and the corresponding frame
        print("Maximum cumulative white pixel count:", np.max(cumulative_white_pixel_counts1))
        print("Time at which this value was reached:", frame_at_max/20, "s")

        # # Plot the number of white pixels per frame
        # plt.figure(figsize=(20, 6))

        # # Plot for white pixels in each frame
        # #plt.subplot(2, 2, 2)  # First subplot
        # plt.plot(frame_counts2, white_pixel_counts2, linestyle='--', color='b')
        # plt.xlabel('Frame Count')
        # plt.ylabel('Number of White Pixels')
        # plt.title('Number of White Pixels per Frame')
        # plt.show()

        # # Plot for cumulative sum of white pixels
        # #plt.subplot(2, 2, 2)  # Second subplot
        # plt.plot(frame_counts2, cumulative_white_pixel_counts2, linestyle='--', color='b')
        # plt.xlabel('Frame Count')
        # plt.ylabel('Cumulative Sum of White Pixels')
        # plt.title('Cumulative Sum of White Pixels')
        # plt.show()

        if ((last_cumulative_count1/10000)*(frame_at_max/20) < 100):
            return False
        else:
            return True

