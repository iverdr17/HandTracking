// Copyright 2019 The MediaPipe Authors.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

package com.google.mediapipe.apps.handtrackinggpu;


import android.os.Bundle;
import android.util.Log;
import android.view.GestureDetector;
import android.view.MotionEvent;

import com.google.mediapipe.apps.basic.calibrate;
import com.google.mediapipe.formats.proto.LandmarkProto.NormalizedLandmark;
import com.google.mediapipe.formats.proto.LandmarkProto.NormalizedLandmarkList;
import com.google.mediapipe.framework.PacketGetter;
import com.google.protobuf.InvalidProtocolBufferException;

import static java.lang.Math.atan;


/** Main activity of MediaPipe hand tracking app. */
public class MainActivity extends com.google.mediapipe.apps.basic.MainActivity implements GestureDetector.OnGestureListener, GestureDetector.OnDoubleTapListener {
  private static final String TAG = "MainActivity";

  private static final String OUTPUT_HAND_PRESENCE_STREAM_NAME = "hand_presence";
  private static final String OUTPUT_LANDMARKS_STREAM_NAME = "hand_landmarks";
  public GestureDetector gestureDetector;

 //   private static final CameraHelper.CameraFacing CAMERA_FACING = CameraHelper.CameraFacing.FRONT;
   // private CameraXPreviewHelper cameraHelper;
 public int b;
    @Override
    public boolean onSingleTapConfirmed(MotionEvent e) {
        return false;
    }

    @Override
    public boolean onDoubleTap(MotionEvent e) {
        b=2;
        return false;
    }

    @Override
    public boolean onDoubleTapEvent(MotionEvent e) {
        return false;
    }

    @Override
    public boolean onDown(MotionEvent e) {
        return false;
    }

    @Override
    public void onShowPress(MotionEvent e) {

    }

    @Override
    public boolean onTouchEvent(MotionEvent event) {
        this.gestureDetector.onTouchEvent(event);
        return super.onTouchEvent(event);
    }

    @Override
    public boolean onScroll(MotionEvent e1, MotionEvent e2, float distanceX, float distanceY) {
        return false;
    }

    @Override
    public void onLongPress(MotionEvent e) {
        b=2;
    }

    @Override
    public boolean onFling(MotionEvent e1, MotionEvent e2, float velocityX, float velocityY) {
        return false;
    }

    @Override
    public boolean onSingleTapUp(MotionEvent e) {
        b=1;
        return (false);
    }

    @Override
  protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    this.gestureDetector = new GestureDetector(this,this);
    processor.addPacketCallback(
        OUTPUT_HAND_PRESENCE_STREAM_NAME,
        (packet) -> {
          Boolean handPresence = PacketGetter.getBool(packet);
          if (!handPresence) {
            Log.d(
                TAG,
                "[TS:" + packet.getTimestamp() + "] Hand presence is false, no hands detected.");

          }
        });

    processor.addPacketCallback(
        OUTPUT_LANDMARKS_STREAM_NAME,
        (packet) -> {
          byte[] landmarksRaw = PacketGetter.getProtoBytes(packet);
          try {
            NormalizedLandmarkList landmarks = NormalizedLandmarkList.parseFrom(landmarksRaw);
             float a[] =   cameraHelper.focallengthinmm();

              float HFOV= (float) (2.0f * atan(a[1] / (2.0f * a[0])));
              float VFOV= (float) (2.0f * atan(a[2] / (2.0f * a[0])));
              String s1= String.valueOf(Math.toDegrees(HFOV)/2);
              String s2= String.valueOf(Math.toDegrees(VFOV)/2);
              Log.d(TAG,"focallengthinmm: ("+s1+","+s2 +")in");
              if (landmarks == null) {
              Log.d(TAG, "[TS:" + packet.getTimestamp() + "] No hand landmarks.");
              return;
            }
            int A[]=calibrate.calib;
            // Note: If hand_presence is false, these landmarks are useless.
            if(b==1)
            {
                Log.d(TAG, getLandmarksDebugString(landmarks)+"TapPress");
                b=0;
            }
            else if (b==2){
                Log.d(TAG, getLandmarksDebugString(landmarks)+"DoublePress");
                b=0;
            }
            else {
                Log.d(TAG, getLandmarksDebugString(landmarks)+"Press");
            }
            } catch (InvalidProtocolBufferException e) {
            //Log.e(TAG, "Couldn't Exception received - " + e);
            return;
          }
        });
  }

    private static String getLandmarksDebugString(NormalizedLandmarkList landmarks) {
        int landmarkIndex = 0;
        String landmarksString = "";
        char detect='a';
        for (NormalizedLandmark landmark : landmarks.getLandmarkList()) {

                landmarksString +=
                        "\t\tLandmark["
                                + landmarkIndex
                                + "]: ("
                                + landmark.getX()
                                + ","
                                + landmark.getY()
                                + "!"
                                + landmark.getZ()
                                + ")" + detect;
                ++landmarkIndex;
                detect++;

        }
 //       landmarksString+="TheEnd   ";
        return landmarksString;
  }
}
