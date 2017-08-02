
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework import mixins
from rest_framework import generics
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse

from cozmo.util import degrees, distance_mm, speed_mmps, Pose
from cozmo.objects import LightCube1Id, LightCube2Id, LightCube3Id

import cozmo
import time
import logging
import json
import sys
import threading

anim_dic = {
    'AcknowledgeFaceInitPause': cozmo.anim.Triggers.AcknowledgeFaceInitPause,
    'AcknowledgeFaceNamed': cozmo.anim.Triggers.AcknowledgeFaceNamed,
    'AcknowledgeFaceUnnamed': cozmo.anim.Triggers.AcknowledgeFaceUnnamed,
    'AcknowledgeObject': cozmo.anim.Triggers.AcknowledgeObject,
    'AskToBeRightedLeft': cozmo.anim.Triggers.AskToBeRightedLeft,
    'AskToBeRightedRight': cozmo.anim.Triggers.AskToBeRightedRight,
    'BlockReact': cozmo.anim.Triggers.BlockReact,
    'BuildPyramidFirstBlockOnSide': cozmo.anim.Triggers.BuildPyramidFirstBlockOnSide,
    'BuildPyramidFirstBlockUpright': cozmo.anim.Triggers.BuildPyramidFirstBlockUpright,
    'BuildPyramidLookForFace': cozmo.anim.Triggers.BuildPyramidLookForFace,
    'BuildPyramidReactToBase': cozmo.anim.Triggers.BuildPyramidReactToBase,
    'BuildPyramidSecondBlockOnSide': cozmo.anim.Triggers.BuildPyramidSecondBlockOnSide,
    'BuildPyramidSecondBlockUpright': cozmo.anim.Triggers.BuildPyramidSecondBlockUpright,
    'BuildPyramidSuccess': cozmo.anim.Triggers.BuildPyramidSuccess,
    'BuildPyramidThankUser': cozmo.anim.Triggers.BuildPyramidThankUser,
    'BuildPyramidThirdBlockOnSide': cozmo.anim.Triggers.BuildPyramidThirdBlockOnSide,
    'BuildPyramidThirdBlockUpright': cozmo.anim.Triggers.BuildPyramidThirdBlockUpright,
    'CantHandleTallStack': cozmo.anim.Triggers.CantHandleTallStack,
    'ConnectWakeUp': cozmo.anim.Triggers.ConnectWakeUp,
    'Count': cozmo.anim.Triggers.Count,
    'CozmoSaysBadWord': cozmo.anim.Triggers.CozmoSaysBadWord,
    'CozmoSaysGetIn': cozmo.anim.Triggers.CozmoSaysGetIn,
    'CozmoSaysGetOut': cozmo.anim.Triggers.CozmoSaysGetOut,
    'CozmoSaysIdle': cozmo.anim.Triggers.CozmoSaysIdle,
    'CozmoSaysSpeakGetInLong': cozmo.anim.Triggers.CozmoSaysSpeakGetInLong,
    'CozmoSaysSpeakGetInMedium': cozmo.anim.Triggers.CozmoSaysSpeakGetInMedium,
    'CozmoSaysSpeakGetInShort': cozmo.anim.Triggers.CozmoSaysSpeakGetInShort,
    'CozmoSaysSpeakGetOutLong': cozmo.anim.Triggers.CozmoSaysSpeakGetOutLong,
    'CozmoSaysSpeakGetOutMedium': cozmo.anim.Triggers.CozmoSaysSpeakGetOutMedium,
    'CozmoSaysSpeakGetOutShort': cozmo.anim.Triggers.CozmoSaysSpeakGetOutShort,
    'CozmoSaysSpeakLoop': cozmo.anim.Triggers.CozmoSaysSpeakLoop,
    'CubeMovedSense': cozmo.anim.Triggers.CubeMovedSense,
    'CubeMovedUpset': cozmo.anim.Triggers.CubeMovedUpset,
    'CubePounceFake': cozmo.anim.Triggers.CubePounceFake,
    'CubePounceGetIn': cozmo.anim.Triggers.CubePounceGetIn,
    'CubePounceGetOut': cozmo.anim.Triggers.CubePounceGetOut,
    'CubePounceGetReady': cozmo.anim.Triggers.CubePounceGetReady,
    'CubePounceGetUnready': cozmo.anim.Triggers.CubePounceGetUnready,
    'CubePounceIdleLiftDown': cozmo.anim.Triggers.CubePounceIdleLiftDown,
    'CubePounceIdleLiftUp': cozmo.anim.Triggers.CubePounceIdleLiftUp,
    'CubePounceLoseHand': cozmo.anim.Triggers.CubePounceLoseHand,
    'CubePounceLoseRound': cozmo.anim.Triggers.CubePounceLoseRound,
    'CubePounceLoseSession': cozmo.anim.Triggers.CubePounceLoseSession,
    'CubePouncePounceClose': cozmo.anim.Triggers.CubePouncePounceClose,
    'CubePouncePounceNormal': cozmo.anim.Triggers.CubePouncePounceNormal,
    'CubePounceWinHand': cozmo.anim.Triggers.CubePounceWinHand,
    'CubePounceWinRound': cozmo.anim.Triggers.CubePounceWinRound,
    'CubePounceWinSession': cozmo.anim.Triggers.CubePounceWinSession,
    'DemoSpeedTapCozmoLose': cozmo.anim.Triggers.DemoSpeedTapCozmoLose,
    'DemoSpeedTapCozmoWin': cozmo.anim.Triggers.DemoSpeedTapCozmoWin,
    'DizzyReactionHard': cozmo.anim.Triggers.DizzyReactionHard,
    'DizzyReactionMedium': cozmo.anim.Triggers.DizzyReactionMedium,
    'DizzyReactionSoft': cozmo.anim.Triggers.DizzyReactionSoft,
    'DizzyShakeLoop': cozmo.anim.Triggers.DizzyShakeLoop,
    'DizzyShakeStop': cozmo.anim.Triggers.DizzyShakeStop,
    'DizzyStillPickedUp': cozmo.anim.Triggers.DizzyStillPickedUp,
    'DriveEndAngry': cozmo.anim.Triggers.DriveEndAngry,
    'DriveEndDefault': cozmo.anim.Triggers.DriveEndDefault,
    'DriveEndLaunch': cozmo.anim.Triggers.DriveEndLaunch,
    'DriveLoopAngry': cozmo.anim.Triggers.DriveLoopAngry,
    'DriveLoopDefault': cozmo.anim.Triggers.DriveLoopDefault,
    'DriveLoopLaunch': cozmo.anim.Triggers.DriveLoopLaunch,
    'DriveStartAngry': cozmo.anim.Triggers.DriveStartAngry,
    'DriveStartDefault': cozmo.anim.Triggers.DriveStartDefault,
    'DriveStartLaunch': cozmo.anim.Triggers.DriveStartLaunch,
    'DroneModeBackwardDrivingEnd': cozmo.anim.Triggers.DroneModeBackwardDrivingEnd,
    'DroneModeBackwardDrivingLoop': cozmo.anim.Triggers.DroneModeBackwardDrivingLoop,
    'DroneModeBackwardDrivingStart': cozmo.anim.Triggers.DroneModeBackwardDrivingStart,
    'DroneModeCliffEvent': cozmo.anim.Triggers.DroneModeCliffEvent,
    'DroneModeForwardDrivingEnd': cozmo.anim.Triggers.DroneModeForwardDrivingEnd,
    'DroneModeForwardDrivingLoop': cozmo.anim.Triggers.DroneModeForwardDrivingLoop,
    'DroneModeForwardDrivingStart': cozmo.anim.Triggers.DroneModeForwardDrivingStart,
    'DroneModeGetIn': cozmo.anim.Triggers.DroneModeGetIn,
    'DroneModeGetOut': cozmo.anim.Triggers.DroneModeGetOut,
    'DroneModeIdle': cozmo.anim.Triggers.DroneModeIdle,
    'DroneModeKeepAlive': cozmo.anim.Triggers.DroneModeKeepAlive,
    'DroneModeTurboDrivingStart': cozmo.anim.Triggers.DroneModeTurboDrivingStart,
    'FacePlantRoll': cozmo.anim.Triggers.FacePlantRoll,
    'FacePlantRollArmUp': cozmo.anim.Triggers.FacePlantRollArmUp,
    'FailedToRightFromFace': cozmo.anim.Triggers.FailedToRightFromFace,
    'FistBumpIdle': cozmo.anim.Triggers.FistBumpIdle,
    'FistBumpLeftHanging': cozmo.anim.Triggers.FistBumpLeftHanging,
    'FistBumpRequestOnce': cozmo.anim.Triggers.FistBumpRequestOnce,
    'FistBumpRequestRetry': cozmo.anim.Triggers.FistBumpRequestRetry,
    'FistBumpSuccess': cozmo.anim.Triggers.FistBumpSuccess,
    'FlipDownFromBack': cozmo.anim.Triggers.FlipDownFromBack,
    'FrustratedByFailure': cozmo.anim.Triggers.FrustratedByFailure,
    'FrustratedByFailureMajor': cozmo.anim.Triggers.FrustratedByFailureMajor,
    'GameSetupGetIn': cozmo.anim.Triggers.GameSetupGetIn,
    'GameSetupGetOut': cozmo.anim.Triggers.GameSetupGetOut,
    'GameSetupIdle': cozmo.anim.Triggers.GameSetupIdle,
    'GameSetupReaction': cozmo.anim.Triggers.GameSetupReaction,
    'GoToSleepGetIn': cozmo.anim.Triggers.GoToSleepGetIn,
    'GoToSleepGetOut': cozmo.anim.Triggers.GoToSleepGetOut,
    'GoToSleepOff': cozmo.anim.Triggers.GoToSleepOff,
    'GoToSleepSleeping': cozmo.anim.Triggers.GoToSleepSleeping,
    'GuardDogBusted': cozmo.anim.Triggers.GuardDogBusted,
    'GuardDogCubeDisconnect': cozmo.anim.Triggers.GuardDogCubeDisconnect,
    'GuardDogFakeout': cozmo.anim.Triggers.GuardDogFakeout,
    'GuardDogInterruption': cozmo.anim.Triggers.GuardDogInterruption,
    'GuardDogPlayerSuccess': cozmo.anim.Triggers.GuardDogPlayerSuccess,
    'GuardDogPulse': cozmo.anim.Triggers.GuardDogPulse,
    'GuardDogSettle': cozmo.anim.Triggers.GuardDogSettle,
    'GuardDogSleepLoop': cozmo.anim.Triggers.GuardDogSleepLoop,
    'GuardDogTimeout': cozmo.anim.Triggers.GuardDogTimeout,
    'GuardDogTimeoutCubesTouched': cozmo.anim.Triggers.GuardDogTimeoutCubesTouched,
    'GuardDogTimeoutCubesUntouched': cozmo.anim.Triggers.GuardDogTimeoutCubesUntouched,
    'Hiccup': cozmo.anim.Triggers.Hiccup,
    'HiccupGetIn': cozmo.anim.Triggers.HiccupGetIn,
    'HiccupPlayerCure': cozmo.anim.Triggers.HiccupPlayerCure,
    'HiccupRobotOnBack': cozmo.anim.Triggers.HiccupRobotOnBack,
    'HiccupRobotOnFace': cozmo.anim.Triggers.HiccupRobotOnFace,
    'HiccupRobotPickedUp': cozmo.anim.Triggers.HiccupRobotPickedUp,
    'HiccupSelfCure': cozmo.anim.Triggers.HiccupSelfCure,
    'HikingDrivingEnd': cozmo.anim.Triggers.HikingDrivingEnd,
    'HikingDrivingLoop': cozmo.anim.Triggers.HikingDrivingLoop,
    'HikingDrivingStart': cozmo.anim.Triggers.HikingDrivingStart,
    'HikingInterestingEdgeThought': cozmo.anim.Triggers.HikingInterestingEdgeThought,
    'HikingIntro': cozmo.anim.Triggers.HikingIntro,
    'HikingLookAround': cozmo.anim.Triggers.HikingLookAround,
    'HikingObserve': cozmo.anim.Triggers.HikingObserve,
    'HikingReactToEdge': cozmo.anim.Triggers.HikingReactToEdge,
    'HikingReactToNewArea': cozmo.anim.Triggers.HikingReactToNewArea,
    'HikingReactToPossibleMarker': cozmo.anim.Triggers.HikingReactToPossibleMarker,
    'HikingSquintEnd': cozmo.anim.Triggers.HikingSquintEnd,
    'HikingSquintLoop': cozmo.anim.Triggers.HikingSquintLoop,
    'HikingSquintStart': cozmo.anim.Triggers.HikingSquintStart,
    'HikingWakeUpOffCharger': cozmo.anim.Triggers.HikingWakeUpOffCharger,
    'IdleOnCharger': cozmo.anim.Triggers.IdleOnCharger,
    'InteractWithFaceTrackingIdle': cozmo.anim.Triggers.InteractWithFaceTrackingIdle,
    'InteractWithFacesInitialNamed': cozmo.anim.Triggers.InteractWithFacesInitialNamed,
    'InteractWithFacesInitialUnnamed': cozmo.anim.Triggers.InteractWithFacesInitialUnnamed,
    'KnockOverEyes': cozmo.anim.Triggers.KnockOverEyes,
    'KnockOverFailure': cozmo.anim.Triggers.KnockOverFailure,
    'KnockOverGrabAttempt': cozmo.anim.Triggers.KnockOverGrabAttempt,
    'KnockOverPreActionNamedFace': cozmo.anim.Triggers.KnockOverPreActionNamedFace,
    'KnockOverPreActionUnnamedFace': cozmo.anim.Triggers.KnockOverPreActionUnnamedFace,
    'KnockOverSuccess': cozmo.anim.Triggers.KnockOverSuccess,
    'LookInPlaceForFacesBodyPause': cozmo.anim.Triggers.LookInPlaceForFacesBodyPause,
    'LookInPlaceForFacesHeadMovePause': cozmo.anim.Triggers.LookInPlaceForFacesHeadMovePause,
    'MajorFail': cozmo.anim.Triggers.MajorFail,
    'MajorWin': cozmo.anim.Triggers.MajorWin,
    'MeetCozmoFirstEnrollmentCelebration': cozmo.anim.Triggers.MeetCozmoFirstEnrollmentCelebration,
    'MeetCozmoFirstEnrollmentRepeatName': cozmo.anim.Triggers.MeetCozmoFirstEnrollmentRepeatName,
    'MeetCozmoFirstEnrollmentSayName': cozmo.anim.Triggers.MeetCozmoFirstEnrollmentSayName,
    'MeetCozmoGetIn': cozmo.anim.Triggers.MeetCozmoGetIn,
    'MeetCozmoLookFaceGetIn': cozmo.anim.Triggers.MeetCozmoLookFaceGetIn,
    'MeetCozmoLookFaceGetOut': cozmo.anim.Triggers.MeetCozmoLookFaceGetOut,
    'MeetCozmoLookFaceInterrupt': cozmo.anim.Triggers.MeetCozmoLookFaceInterrupt,
    'MeetCozmoReEnrollmentSayName': cozmo.anim.Triggers.MeetCozmoReEnrollmentSayName,
    'MeetCozmoRenameFaceSayName': cozmo.anim.Triggers.MeetCozmoRenameFaceSayName,
    'MeetCozmoScanningIdle': cozmo.anim.Triggers.MeetCozmoScanningIdle,
    'MemoryMatchCozmoFollowTapsSoundOnly': cozmo.anim.Triggers.MemoryMatchCozmoFollowTapsSoundOnly,
    'MemoryMatchCozmoGetOut': cozmo.anim.Triggers.MemoryMatchCozmoGetOut,
    'MemoryMatchCozmoLoseHand': cozmo.anim.Triggers.MemoryMatchCozmoLoseHand,
    'MemoryMatchCozmoWinGame': cozmo.anim.Triggers.MemoryMatchCozmoWinGame,
    'MemoryMatchCozmoWinHand': cozmo.anim.Triggers.MemoryMatchCozmoWinHand,
    'MemoryMatchPlayerLoseHand': cozmo.anim.Triggers.MemoryMatchPlayerLoseHand,
    'MemoryMatchPlayerLoseHandSolo': cozmo.anim.Triggers.MemoryMatchPlayerLoseHandSolo,
    'MemoryMatchPlayerWinGame': cozmo.anim.Triggers.MemoryMatchPlayerWinGame,
    'MemoryMatchPlayerWinHand': cozmo.anim.Triggers.MemoryMatchPlayerWinHand,
    'MemoryMatchPlayerWinHandLong': cozmo.anim.Triggers.MemoryMatchPlayerWinHandLong,
    'MemoryMatchPlayerWinHandSolo': cozmo.anim.Triggers.MemoryMatchPlayerWinHandSolo,
    'MemoryMatchPointCenter': cozmo.anim.Triggers.MemoryMatchPointCenter,
    'MemoryMatchPointCenterFast': cozmo.anim.Triggers.MemoryMatchPointCenterFast,
    'MemoryMatchPointLeftBig': cozmo.anim.Triggers.MemoryMatchPointLeftBig,
    'MemoryMatchPointLeftBigFast': cozmo.anim.Triggers.MemoryMatchPointLeftBigFast,
    'MemoryMatchPointLeftSmall': cozmo.anim.Triggers.MemoryMatchPointLeftSmall,
    'MemoryMatchPointLeftSmallFast': cozmo.anim.Triggers.MemoryMatchPointLeftSmallFast,
    'MemoryMatchPointRightBig': cozmo.anim.Triggers.MemoryMatchPointRightBig,
    'MemoryMatchPointRightBigFast': cozmo.anim.Triggers.MemoryMatchPointRightBigFast,
    'MemoryMatchPointRightSmall': cozmo.anim.Triggers.MemoryMatchPointRightSmall,
    'MemoryMatchPointRightSmallFast': cozmo.anim.Triggers.MemoryMatchPointRightSmallFast,
    'MemoryMatchReactToPattern': cozmo.anim.Triggers.MemoryMatchReactToPattern,
    'MemoryMatchReactToPatternSolo': cozmo.anim.Triggers.MemoryMatchReactToPatternSolo,
    'MemoryMatchSoloGameOver': cozmo.anim.Triggers.MemoryMatchSoloGameOver,
    'NamedFaceInitialGreeting': cozmo.anim.Triggers.NamedFaceInitialGreeting,
    'NeutralFace': cozmo.anim.Triggers.NeutralFace,
    'NothingToDoBoredEvent': cozmo.anim.Triggers.NothingToDoBoredEvent,
    'NothingToDoBoredIdle': cozmo.anim.Triggers.NothingToDoBoredIdle,
    'NothingToDoBoredIntro': cozmo.anim.Triggers.NothingToDoBoredIntro,
    'NothingToDoBoredOutro': cozmo.anim.Triggers.NothingToDoBoredOutro,
    'OnLearnedPlayerName': cozmo.anim.Triggers.OnLearnedPlayerName,
    'OnSawNewNamedFace': cozmo.anim.Triggers.OnSawNewNamedFace,
    'OnSawNewUnnamedFace': cozmo.anim.Triggers.OnSawNewUnnamedFace,
    'OnSawOldNamedFace': cozmo.anim.Triggers.OnSawOldNamedFace,
    'OnSawOldUnnamedFace': cozmo.anim.Triggers.OnSawOldUnnamedFace,
    'OnSpeedtapCozmoConfirm': cozmo.anim.Triggers.OnSpeedtapCozmoConfirm,
    'OnSpeedtapFakeout': cozmo.anim.Triggers.OnSpeedtapFakeout,
    'OnSpeedtapGameCozmoWinHighIntensity': cozmo.anim.Triggers.OnSpeedtapGameCozmoWinHighIntensity,
    'OnSpeedtapGameCozmoWinLowIntensity': cozmo.anim.Triggers.OnSpeedtapGameCozmoWinLowIntensity,
    'OnSpeedtapGamePlayerWinHighIntensity': cozmo.anim.Triggers.OnSpeedtapGamePlayerWinHighIntensity,
    'OnSpeedtapGamePlayerWinLowIntensity': cozmo.anim.Triggers.OnSpeedtapGamePlayerWinLowIntensity,
    'OnSpeedtapGetOut': cozmo.anim.Triggers.OnSpeedtapGetOut,
    'OnSpeedtapHandCozmoWin': cozmo.anim.Triggers.OnSpeedtapHandCozmoWin,
    'OnSpeedtapHandPlayerWin': cozmo.anim.Triggers.OnSpeedtapHandPlayerWin,
    'OnSpeedtapIdle': cozmo.anim.Triggers.OnSpeedtapIdle,
    'OnSpeedtapRoundCozmoWinHighIntensity': cozmo.anim.Triggers.OnSpeedtapRoundCozmoWinHighIntensity,
    'OnSpeedtapRoundCozmoWinLowIntensity': cozmo.anim.Triggers.OnSpeedtapRoundCozmoWinLowIntensity,
    'OnSpeedtapRoundPlayerWinHighIntensity': cozmo.anim.Triggers.OnSpeedtapRoundPlayerWinHighIntensity,
    'OnSpeedtapRoundPlayerWinLowIntensity': cozmo.anim.Triggers.OnSpeedtapRoundPlayerWinLowIntensity,
    'OnSpeedtapTap': cozmo.anim.Triggers.OnSpeedtapTap,
    'OnWaitForCubesMinigameSetup': cozmo.anim.Triggers.OnWaitForCubesMinigameSetup,
    'OnWiggle': cozmo.anim.Triggers.OnWiggle,
    'OnboardingBirth': cozmo.anim.Triggers.OnboardingBirth,
    'OnboardingCubeDockFail': cozmo.anim.Triggers.OnboardingCubeDockFail,
    'OnboardingDiscoverCube': cozmo.anim.Triggers.OnboardingDiscoverCube,
    'OnboardingDriveEnd': cozmo.anim.Triggers.OnboardingDriveEnd,
    'OnboardingDriveLoop': cozmo.anim.Triggers.OnboardingDriveLoop,
    'OnboardingDriveStart': cozmo.anim.Triggers.OnboardingDriveStart,
    'OnboardingEyesOn': cozmo.anim.Triggers.OnboardingEyesOn,
    'OnboardingGetOut': cozmo.anim.Triggers.OnboardingGetOut,
    'OnboardingHelloPlayer': cozmo.anim.Triggers.OnboardingHelloPlayer,
    'OnboardingHelloWorld': cozmo.anim.Triggers.OnboardingHelloWorld,
    'OnboardingIdle': cozmo.anim.Triggers.OnboardingIdle,
    'OnboardingInteractWithCube': cozmo.anim.Triggers.OnboardingInteractWithCube,
    'OnboardingPreBirth': cozmo.anim.Triggers.OnboardingPreBirth,
    'OnboardingReactToCube': cozmo.anim.Triggers.OnboardingReactToCube,
    'OnboardingReactToCubePutDown': cozmo.anim.Triggers.OnboardingReactToCubePutDown,
    'OnboardingReactToFace': cozmo.anim.Triggers.OnboardingReactToFace,
    'OnboardingSoundOnlyLiftEffortPickup': cozmo.anim.Triggers.OnboardingSoundOnlyLiftEffortPickup,
    'OnboardingSoundOnlyLiftEffortPlaceLow': cozmo.anim.Triggers.OnboardingSoundOnlyLiftEffortPlaceLow,
    'PatternGuessNewIdea': cozmo.anim.Triggers.PatternGuessNewIdea,
    'PatternGuessThinking': cozmo.anim.Triggers.PatternGuessThinking,
    'PeekABooGetIn': cozmo.anim.Triggers.PeekABooGetIn,
    'PeekABooGetOutHappy': cozmo.anim.Triggers.PeekABooGetOutHappy,
    'PeekABooGetOutSad': cozmo.anim.Triggers.PeekABooGetOutSad,
    'PeekABooHighIntensity': cozmo.anim.Triggers.PeekABooHighIntensity,
    'PeekABooIdle': cozmo.anim.Triggers.PeekABooIdle,
    'PeekABooLowIntensity': cozmo.anim.Triggers.PeekABooLowIntensity,
    'PeekABooMedIntensity': cozmo.anim.Triggers.PeekABooMedIntensity,
    'PeekABooNoUserInteraction': cozmo.anim.Triggers.PeekABooNoUserInteraction,
    'PeekABooShort': cozmo.anim.Triggers.PeekABooShort,
    'PeekABooSurprised': cozmo.anim.Triggers.PeekABooSurprised,
    'PetDetectionCat': cozmo.anim.Triggers.PetDetectionCat,
    'PetDetectionDog': cozmo.anim.Triggers.PetDetectionDog,
    'PetDetectionShort': cozmo.anim.Triggers.PetDetectionShort,
    'PetDetectionShort_Cat': cozmo.anim.Triggers.PetDetectionShort_Cat,
    'PetDetectionShort_Dog': cozmo.anim.Triggers.PetDetectionShort_Dog,
    'PetDetectionSneeze': cozmo.anim.Triggers.PetDetectionSneeze,
    'PlacedOnCharger': cozmo.anim.Triggers.PlacedOnCharger,
    'PopAWheelieInitial': cozmo.anim.Triggers.PopAWheelieInitial,
    'PopAWheeliePreActionNamedFace': cozmo.anim.Triggers.PopAWheeliePreActionNamedFace,
    'PopAWheeliePreActionUnnamedFace': cozmo.anim.Triggers.PopAWheeliePreActionUnnamedFace,
    'PopAWheelieRealign': cozmo.anim.Triggers.PopAWheelieRealign,
    'PopAWheelieRetry': cozmo.anim.Triggers.PopAWheelieRetry,
    'PounceDriveEnd': cozmo.anim.Triggers.PounceDriveEnd,
    'PounceDriveLoop': cozmo.anim.Triggers.PounceDriveLoop,
    'PounceDriveStart': cozmo.anim.Triggers.PounceDriveStart,
    'PounceFace': cozmo.anim.Triggers.PounceFace,
    'PounceFail': cozmo.anim.Triggers.PounceFail,
    'PounceGetOut': cozmo.anim.Triggers.PounceGetOut,
    'PounceInitial': cozmo.anim.Triggers.PounceInitial,
    'PouncePounce': cozmo.anim.Triggers.PouncePounce,
    'PounceSuccess': cozmo.anim.Triggers.PounceSuccess,
    'ProceduralLive': cozmo.anim.Triggers.ProceduralLive,
    'PutDownBlockKeepAlive': cozmo.anim.Triggers.PutDownBlockKeepAlive,
    'PutDownBlockPutDown': cozmo.anim.Triggers.PutDownBlockPutDown,
    'ReactToBlockPickupSuccess': cozmo.anim.Triggers.ReactToBlockPickupSuccess,
    'ReactToBlockRetryPickup': cozmo.anim.Triggers.ReactToBlockRetryPickup,
    'ReactToCliff': cozmo.anim.Triggers.ReactToCliff,
    'ReactToCliffDetectorStop': cozmo.anim.Triggers.ReactToCliffDetectorStop,
    'ReactToMotorCalibration': cozmo.anim.Triggers.ReactToMotorCalibration,
    'ReactToNewBlockAsk': cozmo.anim.Triggers.ReactToNewBlockAsk,
    'ReactToNewBlockBig': cozmo.anim.Triggers.ReactToNewBlockBig,
    'ReactToNewBlockSmall': cozmo.anim.Triggers.ReactToNewBlockSmall,
    'ReactToOnLeftSide': cozmo.anim.Triggers.ReactToOnLeftSide,
    'ReactToOnRightSide': cozmo.anim.Triggers.ReactToOnRightSide,
    'ReactToPerchedOnBlock': cozmo.anim.Triggers.ReactToPerchedOnBlock,
    'ReactToPickup': cozmo.anim.Triggers.ReactToPickup,
    'ReactToPokeReaction': cozmo.anim.Triggers.ReactToPokeReaction,
    'ReactToPokeStartled': cozmo.anim.Triggers.ReactToPokeStartled,
    'ReactToUnexpectedMovement': cozmo.anim.Triggers.ReactToUnexpectedMovement,
    'RequestGameKeepAwayAccept0': cozmo.anim.Triggers.RequestGameKeepAwayAccept0,
    'RequestGameKeepAwayAccept1': cozmo.anim.Triggers.RequestGameKeepAwayAccept1,
    'RequestGameKeepAwayDeny0': cozmo.anim.Triggers.RequestGameKeepAwayDeny0,
    'RequestGameKeepAwayDeny1': cozmo.anim.Triggers.RequestGameKeepAwayDeny1,
    'RequestGameKeepAwayIdle0': cozmo.anim.Triggers.RequestGameKeepAwayIdle0,
    'RequestGameKeepAwayIdle1': cozmo.anim.Triggers.RequestGameKeepAwayIdle1,
    'RequestGameKeepAwayInitial0': cozmo.anim.Triggers.RequestGameKeepAwayInitial0,
    'RequestGameKeepAwayInitial1': cozmo.anim.Triggers.RequestGameKeepAwayInitial1,
    'RequestGameKeepAwayPreDrive0': cozmo.anim.Triggers.RequestGameKeepAwayPreDrive0,
    'RequestGameKeepAwayPreDrive1': cozmo.anim.Triggers.RequestGameKeepAwayPreDrive1,
    'RequestGameKeepAwayRequest0': cozmo.anim.Triggers.RequestGameKeepAwayRequest0,
    'RequestGameKeepAwayRequest1': cozmo.anim.Triggers.RequestGameKeepAwayRequest1,
    'RequestGameMemoryMatchAccept0': cozmo.anim.Triggers.RequestGameMemoryMatchAccept0,
    'RequestGameMemoryMatchAccept1': cozmo.anim.Triggers.RequestGameMemoryMatchAccept1,
    'RequestGameMemoryMatchDeny0': cozmo.anim.Triggers.RequestGameMemoryMatchDeny0,
    'RequestGameMemoryMatchDeny1': cozmo.anim.Triggers.RequestGameMemoryMatchDeny1,
    'RequestGameMemoryMatchIdle0': cozmo.anim.Triggers.RequestGameMemoryMatchIdle0,
    'RequestGameMemoryMatchIdle1': cozmo.anim.Triggers.RequestGameMemoryMatchIdle1,
    'RequestGameMemoryMatchInitial0': cozmo.anim.Triggers.RequestGameMemoryMatchInitial0,
    'RequestGameMemoryMatchInitial1': cozmo.anim.Triggers.RequestGameMemoryMatchInitial1,
    'RequestGameMemoryMatchPreDrive0': cozmo.anim.Triggers.RequestGameMemoryMatchPreDrive0,
    'RequestGameMemoryMatchPreDrive1': cozmo.anim.Triggers.RequestGameMemoryMatchPreDrive1,
    'RequestGameMemoryMatchRequest0': cozmo.anim.Triggers.RequestGameMemoryMatchRequest0,
    'RequestGameMemoryMatchRequest1': cozmo.anim.Triggers.RequestGameMemoryMatchRequest1,
    'RequestGamePickupFail': cozmo.anim.Triggers.RequestGamePickupFail,
    'RequestGameSpeedTapAccept0': cozmo.anim.Triggers.RequestGameSpeedTapAccept0,
    'RequestGameSpeedTapAccept1': cozmo.anim.Triggers.RequestGameSpeedTapAccept1,
    'RequestGameSpeedTapDeny0': cozmo.anim.Triggers.RequestGameSpeedTapDeny0,
    'RequestGameSpeedTapDeny1': cozmo.anim.Triggers.RequestGameSpeedTapDeny1,
    'RequestGameSpeedTapIdle0': cozmo.anim.Triggers.RequestGameSpeedTapIdle0,
    'RequestGameSpeedTapIdle1': cozmo.anim.Triggers.RequestGameSpeedTapIdle1,
    'RequestGameSpeedTapInitial0': cozmo.anim.Triggers.RequestGameSpeedTapInitial0,
    'RequestGameSpeedTapInitial1': cozmo.anim.Triggers.RequestGameSpeedTapInitial1,
    'RequestGameSpeedTapPreDrive0': cozmo.anim.Triggers.RequestGameSpeedTapPreDrive0,
    'RequestGameSpeedTapPreDrive1': cozmo.anim.Triggers.RequestGameSpeedTapPreDrive1,
    'RequestGameSpeedTapRequest0': cozmo.anim.Triggers.RequestGameSpeedTapRequest0,
    'RequestGameSpeedTapRequest1': cozmo.anim.Triggers.RequestGameSpeedTapRequest1,
    'RollBlockInitial': cozmo.anim.Triggers.RollBlockInitial,
    'RollBlockPreActionNamedFace': cozmo.anim.Triggers.RollBlockPreActionNamedFace,
    'RollBlockPreActionUnnamedFace': cozmo.anim.Triggers.RollBlockPreActionUnnamedFace,
    'RollBlockPutDown': cozmo.anim.Triggers.RollBlockPutDown,
    'RollBlockRealign': cozmo.anim.Triggers.RollBlockRealign,
    'RollBlockRetry': cozmo.anim.Triggers.RollBlockRetry,
    'RollBlockSuccess': cozmo.anim.Triggers.RollBlockSuccess,
    'SdkTextToSpeech': cozmo.anim.Triggers.SdkTextToSpeech,
    'Shiver': cozmo.anim.Triggers.Shiver,
    'Shocked': cozmo.anim.Triggers.Shocked,
    'Sleeping': cozmo.anim.Triggers.Sleeping,
    'SoftSparkUpgradeLift': cozmo.anim.Triggers.SoftSparkUpgradeLift,
    'SoftSparkUpgradeTracks': cozmo.anim.Triggers.SoftSparkUpgradeTracks,
    'SoundOnlyLiftEffortPickup': cozmo.anim.Triggers.SoundOnlyLiftEffortPickup,
    'SoundOnlyLiftEffortPlaceHigh': cozmo.anim.Triggers.SoundOnlyLiftEffortPlaceHigh,
    'SoundOnlyLiftEffortPlaceLow': cozmo.anim.Triggers.SoundOnlyLiftEffortPlaceLow,
    'SoundOnlyLiftEffortPlaceRoll': cozmo.anim.Triggers.SoundOnlyLiftEffortPlaceRoll,
    'SoundOnlyRamIntoBlock': cozmo.anim.Triggers.SoundOnlyRamIntoBlock,
    'SoundOnlyTurnSmall': cozmo.anim.Triggers.SoundOnlyTurnSmall,
    'SparkDrivingLoop': cozmo.anim.Triggers.SparkDrivingLoop,
    'SparkDrivingStart': cozmo.anim.Triggers.SparkDrivingStart,
    'SparkDrivingStop': cozmo.anim.Triggers.SparkDrivingStop,
    'SparkFailure': cozmo.anim.Triggers.SparkFailure,
    'SparkGetIn': cozmo.anim.Triggers.SparkGetIn,
    'SparkGetOut': cozmo.anim.Triggers.SparkGetOut,
    'SparkIdle': cozmo.anim.Triggers.SparkIdle,
    'SparkPickupFinalCubeReaction': cozmo.anim.Triggers.SparkPickupFinalCubeReaction,
    'SparkPickupInitialCubeReaction': cozmo.anim.Triggers.SparkPickupInitialCubeReaction,
    'SparkSuccess': cozmo.anim.Triggers.SparkSuccess,
    'SpeedTapDrivingEnd': cozmo.anim.Triggers.SpeedTapDrivingEnd,
    'SpeedTapDrivingLoop': cozmo.anim.Triggers.SpeedTapDrivingLoop,
    'SpeedTapDrivingStart': cozmo.anim.Triggers.SpeedTapDrivingStart,
    'StackBlocksSuccess': cozmo.anim.Triggers.StackBlocksSuccess,
    'StartSleeping': cozmo.anim.Triggers.StartSleeping,
    'SuccessfulWheelie': cozmo.anim.Triggers.SuccessfulWheelie,
    'Surprise': cozmo.anim.Triggers.Surprise,
    'TurtleRoll': cozmo.anim.Triggers.TurtleRoll,
    'UnitTestAnim': cozmo.anim.Triggers.UnitTestAnim,
    'WaitOnSideLoop': cozmo.anim.Triggers.WaitOnSideLoop,
    'WorkoutPostLift_highEnergy': cozmo.anim.Triggers.WorkoutPostLift_highEnergy,
    'WorkoutPostLift_lowEnergy': cozmo.anim.Triggers.WorkoutPostLift_lowEnergy,
    'WorkoutPostLift_mediumEnergy': cozmo.anim.Triggers.WorkoutPostLift_mediumEnergy,
    'WorkoutPreLift_highEnergy': cozmo.anim.Triggers.WorkoutPreLift_highEnergy,
    'WorkoutPreLift_lowEnergy': cozmo.anim.Triggers.WorkoutPreLift_lowEnergy,
    'WorkoutPreLift_mediumEnergy': cozmo.anim.Triggers.WorkoutPreLift_mediumEnergy,
    'WorkoutPutDown_highEnergy': cozmo.anim.Triggers.WorkoutPutDown_highEnergy,
    'WorkoutPutDown_lowEnergy': cozmo.anim.Triggers.WorkoutPutDown_lowEnergy,
    'WorkoutPutDown_lowEnergy_simple': cozmo.anim.Triggers.WorkoutPutDown_lowEnergy_simple,
    'WorkoutPutDown_mediumEnergy': cozmo.anim.Triggers.WorkoutPutDown_mediumEnergy,
    'WorkoutStrongLift_highEnergy': cozmo.anim.Triggers.WorkoutStrongLift_highEnergy,
    'WorkoutStrongLift_lowEnergy': cozmo.anim.Triggers.WorkoutStrongLift_lowEnergy,
    'WorkoutStrongLift_mediumEnergy': cozmo.anim.Triggers.WorkoutStrongLift_mediumEnergy,
    'WorkoutTransition_highEnergy': cozmo.anim.Triggers.WorkoutTransition_highEnergy,
    'WorkoutTransition_lowEnergy': cozmo.anim.Triggers.WorkoutTransition_lowEnergy,
    'WorkoutTransition_mediumEnergy': cozmo.anim.Triggers.WorkoutTransition_mediumEnergy,
    'WorkoutWeakLift_highEnergy': cozmo.anim.Triggers.WorkoutWeakLift_highEnergy,
    'WorkoutWeakLift_lowEnergy': cozmo.anim.Triggers.WorkoutWeakLift_lowEnergy,
    'WorkoutWeakLift_mediumEnergy': cozmo.anim.Triggers.WorkoutWeakLift_mediumEnergy
}

commands_to_cozmo = None
cozmo_is_busy = False
robot = None
cube_in_lift = None
pose_dict = {}
debug = "ON"

def run_robot(sdk_conn):
    print("Getting Robot access")
    global robot
    global commands_to_cozmo
    robot = sdk_conn.wait_for_robot()
    while True:
        if commands_to_cozmo is not None:
            # Lock the call
            cozmo_is_busy = True
            run_commands(robot, commands_to_cozmo)
            # ResetCommands =None
            commands_to_cozmo = None
            # Unlock
            cozmo_is_busy = False

def run_commands(robot, commands_to_cozmo):
    try:
        for x in commands_to_cozmo['commands']:
            print(x['command'])
            if x['command'] == "ABORT_ACTIONS":
                abort_actions(robot)
                commands_to_cozmo = None
            elif x['command'] == "DEBUG":
                global debug
                debug = x['params'][0]['LEVEL']
                print("Debug has set to %s" % debug)
            elif x['command'] == "WAIT":
                time_to_wait = x['params'][0]['Miliseconds']
                print("Sleep START")
                time.sleep(float(time_to_wait)/1000.0)
                print("Sleep END")
            elif x['command'] == "MOVE_OUT_CHARGE":
                move_out_charger(robot)
            elif x['command'] == "DRIVE_WHEELS":
                speed_left_wheel = x['params'][0]['LEFT']
                speed_right_wheel = x['params'][1]['RIGHT']
                time_to_drive = x['params'][2]['TIME']
                robot_drive_wheels(speed_left_wheel, speed_right_wheel, time_to_drive, robot)
            elif x['command'] == "GO":
                distance_to_go = x['params'][0]['distance']
                speed_to_go = x['params'][1]['speed']
                go(distance_to_go, speed_to_go, robot)
            elif x['command'] == "SPEAK":
                text_to_say = x['params'][0]['text']
                say(text_to_say, robot)
            elif x['command'] == "TURN":
                degrees_to_turn = x['params'][0]['degrees']
                turn(degrees_to_turn, robot)
            elif x['command'] == "MOVE_HEAD":
                degrees_for_head = x['params'][0]['degrees']
                move_robot_head(degrees_for_head, robot)
            elif x['command'] == "SET_BACKPACK_LIGHTS":
                backpack_color = x['params'][0]['color']
                time_for_lights = x['params'][1]['tiempo']
                set_backpack_color(backpack_color, time_for_lights, robot)
            elif x['command'] == "ANIMATION":
                animation_id = x['params'][0]['ANIMATION_ID']
                play_animation(animation_id, robot)
            elif x['command'] == "SET_CUBE_LIGHTS":
                cube_id = x['params'][0]['CUBE_ID']
                color_cube = x['params'][1]['COLOR']
                flash_enable = x['params'][2]['FLASH']
                set_cube_lights(cube_id, color_cube, flash_enable, robot)
            elif x['command'] == "MOVE_LIFT":
                lift_degrees = x['params'][0]['degrees']
                move_cozmo_lift(lift_degrees, robot)
            elif x['command'] == "GO_TO_POSE":
                go_to_axis_x = x['params'][0]['AXIS-X']
                go_to_axis_y = x['params'][1]['AXIS-Y']
                go_to_retry = x['params'][2]['RETRIES']
                go_to_rotation_angle = x['params'][3]['ANGLE']
                cozmo_go_to_pose(go_to_axis_x, go_to_axis_y, go_to_retry, go_to_rotation_angle, robot)
            elif x['command'] == "GO_TO_CUBE":
                cube_to_go = x['params'][0]['CUBE']
                cozmo_go_to_object(cube_to_go, robot)
            elif x['command'] == "CUBE_STACK":
                cube_up = x['params'][0]['CUBE_UP']
                cube_down = x['params'][1]['CUBE_DOWN']
                stack_cubes(cube_up, cube_down, robot)
            elif x['command'] == "PICKUP_CUBE":
                pickup_cube = x['params'][0]['CUBE']
                cozmo_pickup_cube(pickup_cube, robot)
            elif x['command'] == "DROP_CUBE":
                cozmo_drop_cube(robot)
            elif x['command'] == "ROLL_CUBE":
                pickup_cube = x['params'][0]['CUBE']
                cozmo_roll_cube(pickup_cube, robot)
            elif x['command'] == "SAVE_POSE":
                save_pose_id = x['params'][0]['POSE_ID']
                save_pose(save_pose_id, robot)
            elif x['command'] == "REMOVE_POSE":
                save_pose_id = x['params'][0]['POSE_ID']
                remove_pose(save_pose_id, robot)
            elif x['command'] == "GO_POSE":
                save_pose_id = x['params'][0]['POSE_ID']
                go_to_known_pose(save_pose_id, robot)
            else :
                 print("UNKNOWN COMMAND")
    except (ValueError, KeyError, TypeError):
        print("JSON format error")

# -----------------------------------
# FUNCTION: ABORT ALL PENDING ACTIONS
# -----------------------------------

def abort_actions(robot):
    robot.abort_all_actions()
    robot.stop_all_motors()

# -----------------------------------
# FUNCTION: MOVE OUT ROBOT FROM THE CHARGER TO ENABLE MOTION
# -----------------------------------

def move_out_charger(robot):
    robot.drive_off_charger_contacts().wait_for_completed()

# -----------------------------
# FUNCTION: ROBOT TO SAY A TEXT
# -----------------------------

def say(text_to_say, robot):
    print("COZMO TO SAY")
    robot.say_text(text_to_say).wait_for_completed()


# --------------------------------------------------------------------------------------------
# FUNCTION: ROBOT TO MOVE FORWARD "distance_to_go" millimeters WITH SPEED "speed_to_go"
# --------------------------------------------------------------------------------------------

def go(distance_to_go, speed_to_go, robot):
    if debug == "ON":
        print("COZMO TO GO")
        print("    Distance to go = %s " % distance_to_go)
        print("    Speed to go = %s " % speed_to_go)
        print("    Robot = %s " % robot)
    try:
        robot.drive_straight(distance_mm(distance_to_go), speed_mmps(speed_to_go)).wait_for_completed()
        if debug == "ON":
            print("COZMO TO GO COMPLETED")
    except:
        print(sys.exc_info()[0])

# -----------------------------------------------------------------
# FUNCTION: ROBOT TO MOVE SETTING SPEED PER WHEEL SO COZMO CAN TURN
# -----------------------------------------------------------------

def robot_drive_wheels(speed_left_wheel, speed_right_wheel, time_to_drive, robot):
    if debug == "ON":
            print("COZMO DRIVE WHEELS")
            print("    Speed Left = %s " % speed_left_wheel)
            print("    Speed Right= %s " % speed_right_wheel)
            print("    Time To Drive = %s " % time_to_drive)
            print("    Robot = %s " % robot)
    try:
        action = robot.drive_wheels(speed_left_wheel, speed_right_wheel, l_wheel_acc=1000, r_wheel_acc=1000, duration=float(time_to_drive))

        if debug == "ON":
            print("got action", action)
        result = action.wait_for_completed(timeout=30)
        if debug == "ON":
                print("got action result", result)
    except:
        print(sys.exc_info()[0])


# -------------------------------------------------
# FUNCTION: ROBOT TO TURN "degrees_to_turn" DEGREES
# -------------------------------------------------

def turn(degrees_to_turn, robot):
    print("ROTATE COZMO")
    try:
        robot.turn_in_place(degrees(int(degrees_to_turn))).wait_for_completed()
    except:
        print(sys.exc_info()[0])

# -----------------------------------------------------------
# FUNCTION: ROBOT TO MOVE HIS HEAD "degrees_for_head" DEGREES
# -----------------------------------------------------------

def move_robot_head(degrees_for_head, robot):
    print("MOVE COZMO HEAD")
    try:
        robot.set_head_angle(degrees(int(degrees_for_head))).wait_for_completed()
    except:
        print(sys.exc_info()[0])

# -----------------------------------------------------------------------------------------------------
# FUNCTION: ROBOT TO TURN ON BACKPACK LIGHTS IN COLOR "backpack_color" DURING "time_for_lights" SECONDS
# -----------------------------------------------------------------------------------------------------

def set_backpack_color(backpack_color, time_for_lights, robot):
    print("Seting backpack lights")
    if backpack_color == "RED":
        print("Seting backpack lights to RED")
        robot.set_all_backpack_lights(cozmo.lights.red_light)
        time.sleep(int(time_for_lights))
    elif backpack_color == "GREEN":
        print("Seting backpack lights to GREEN")
        robot.set_all_backpack_lights(cozmo.lights.green_light)
        time.sleep(int(time_for_lights))
    elif backpack_color == "BLUE":
        print("Seting backpack lights to BLUE")
        robot.set_all_backpack_lights(cozmo.lights.blue_light)
        time.sleep(int(time_for_lights))
    elif backpack_color == "WHITE":
        print("Seting backpack lights to WHITE")
        robot.set_center_backpack_lights(cozmo.lights.white_light)
        time.sleep(int(time_for_lights))
    else:
        print("Seting backpack lights OFF")
        robot.set_all_backpack_lights(cozmo.lights.off_light)
        time.sleep(int(time_for_lights))

# ------------------------------------
# FUNCTION: ROBOT TO PLAY AN ANIMATION
# ------------------------------------

def play_animation(animation_id, robot):
    print("PLAYING ANIMATION %s" % animation_id)
    global anim_dic
    robot.play_anim_trigger(anim_dic.get(animation_id)).wait_for_completed()

# -----------------------------------------------------------------------------------------------------
# FUNCTION: TURN ON THE LIGHT FOR CUBE "cube_id" IN COLOR "color_cube" DURING "color_cube_time" SECONDS
# -----------------------------------------------------------------------------------------------------

def set_cube_lights(cube_id, color_cube, flash_enable, robot):
    print("SETTING CUBE LIGHTS")
    cube_light_1= robot.world.get_light_cube(LightCube1Id)
    cube_light_2= robot.world.get_light_cube(LightCube2Id)
    cube_light_3= robot.world.get_light_cube(LightCube3Id)
    if cube_id == str(cube_light_1.object_id()):
        print("SETTING CUBE LIGHTS FOR CUBE 1")
        cube_to_set_light = cube_light_1
    elif cube_id == str(cube_light_2.object_id()):
        print("SETTING CUBE LIGHTS FOR CUBE 2")
        cube_to_set_light = cube_light_2
    else:
        print("SETTING CUBE LIGHTS FOR CUBE 3")
        cube_to_set_light = cube_light_3

    print("A ver que CUBE ENCIENDO... %s" % str(cube_to_set_light.object_id))

    if color_cube == "RED":
        if flash_enable == "YES":
            cube_to_set_light.set_lights(cozmo.lights.red_light.flash())
        else:
            cube_to_set_light.set_lights(cozmo.lights.red_light)
    elif color_cube == "BLUE":
        if flash_enable == "YES":
            cube_to_set_light.set_lights(cozmo.lights.blue_light.flash())
        else:
            cube_to_set_light.set_lights(cozmo.lights.blue_light)
    elif color_cube == "GREEN":
        if flash_enable == "YES":
            cube_to_set_light.set_lights(cozmo.lights.green_light.flash())
        else:
            cube_to_set_light.set_lights(cozmo.lights.green_light)
    else:
        cube_to_set_light.set_light_corners(None, None, None, None)
# -------------------------------------------------------
# FUNCTION: ROBOT TO MOVE HIS LIFT "lift_degrees" DEGREES
# -------------------------------------------------------

def move_cozmo_lift(lift_degrees , robot):
    print("MOVING COZMO LIFT")
    robot.move_lift(lift_degrees)

# -----------------------------------------------------------------------------------
# FUNCTION: ROBOT GO TO "AXIS-X, AXIS-Y, RETRY, ROTATION_ANGLE" FROM CURRENT POSITION
# -----------------------------------------------------------------------------------

def cozmo_go_to_pose(go_to_axis_x, go_to_axis_y, go_to_retry, go_to_rotation_angle, robot):
    print("SENDING COZMO TO POSE")
    try:
        robot.go_to_pose(Pose(int(go_to_axis_x), int(go_to_axis_y), int(go_to_retry), angle_z=degrees(int(go_to_rotation_angle))), relative_to_robot=True).wait_for_completed()
    except:
        print(sys.exc_info()[0])

# -----------------------------
# FUNTION: ROBOT TO FIND A CUBE
#------------------------------

def find_cube(cube_number, robot):
    print("SEARCHING CUBE %s" % cube_number)

    # Lookaround until Cozmo knows where at least 2 cubes are:
    lookaround = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
    cubes = None
    cubes = robot.world.wait_until_observe_num_objects(num=3, object_type=cozmo.objects.LightCube, timeout=30)
    lookaround.stop()

    if len(cubes) < 1:
        print ("CUBE NOT FOUND")
        robot.play_anim_trigger(cozmo.anim.Triggers.MajorFail).wait_for_completed()
        return None
    else:
        cube_found = None
        for cube in cubes:
            if (str(cube.object_id) == str(cube_number)):
                print("ENCONTRADO EL CUBO QUE BUSCO: %s" %  str(cube.object_id))
                cube_found = cube

    if cube_found:
        print("Return Cube %s" % str(cube.object_id))
        return cube_found
    else:
        print ("CUBE NOT FOUND")
        robot.play_anim_trigger(cozmo.anim.Triggers.MajorFail).wait_for_completed()
        return None

# ----------------------------
# FUNCTION: ROBOT GO TO OBJECT
# ----------------------------

def cozmo_go_to_object(cube_to_go, robot):
    print("SENDING COZMO TO OBJECT %s" % cube_to_go)

    cube_detination = find_cube(cube_to_go, robot)
    if cube_detination:
        # Drive to 70mm away from the cube (much closer and Cozmo
        # will likely hit the cube) and then stop.
        cube_detination.set_lights(cozmo.lights.green_light)
        action = robot.go_to_object(cube_detination, distance_mm(70.0))
        action.wait_for_completed()
        print("Completed action: result = %s" % action)
        print("Done.")

    else:
        print ("CUBE NOT FOUND!!!!")

# -----------------------------
# FUNTION: ROBOT TO PICKUP CUBE
#------------------------------

def cozmo_pickup_cube(cube_to_pickup, robot):
    print("COZMO TO PICKUP CUBE %s" % str(cube_to_pickup))

    cube_found = find_cube(cube_to_pickup, robot)
    if cube_found:
        print ("CUBE FOUND!!")
        # cube_found.set_lights(cozmo.lights.green_light.flash())
        #initial_pose = robot.pose
        action = robot.pickup_object(cube_found, num_retries=3)
        print("got action", action)
        result = action.wait_for_completed(timeout=30)
        print("got action result", result)
        global cube_in_lift
        cube_in_lift = cube_found
        #robot.go_to_pose(initial_pose).wait_for_completed()
        #robot.turn_in_place(degrees(90)).wait_for_completed()
        # cube_found.set_light_corners(None, None, None, None)
    else:
        print ("CUBE NOT Found")

# -----------------------------
# FUNTION: ROBOT TO DROP CUBE
#------------------------------

def cozmo_drop_cube(robot):
    global cube_in_lift
    if debug == "ON":
        print("COZMO TO DROP CUBE %s " % cube_in_lift)
    action = robot.place_object_on_ground_here(cube_in_lift)
    print("got action", action)
    result = action.wait_for_completed(timeout=30)
    print("got action result", result)

    cube_in_lift = None

# ---------------------------------
# FUNTION: ROBOT TO STACK TWO CUBES
#----------------------------------

def stack_cubes(cube_up, cube_down, robot):
    print("COZMO TRYING TO STACK TWO CUBES")

    # Lookaround until Cozmo knows where at least 2 cubes are:
    lookaround = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
    cubes = robot.world.wait_until_observe_num_objects(num=3, object_type=cozmo.objects.LightCube, timeout=60)
    lookaround.stop()

    if len(cubes) < 2:
        print("Error: need 2 Cubes but only found", len(cubes), "Cube(s)")
    else:
        cube_to_up = None
        cube_to_down = None
        for cube in cubes:
            if (str(cube.object_id) == str(cube_up)):
                cube_to_up = cube
            elif (str(cube.object_id) == str(cube_down)):
                cube_to_down = cube

        if (cube_to_up and cube_to_down):

            action_pickup = robot.pickup_object(cube_to_up)
            action_pickup.wait_for_completed()
            if action_pickup.has_failed:
                code, reason = action_pickup.failure_reason
                result = action_pickup.result
                print("Pickup Cube failed: code=%s reason='%s' result=%s" % (code, reason, result))
                return

            action_down = robot.place_on_object(cube_to_down)
            action_down.wait_for_completed()
            if action_down.has_failed:
                code, reason = action_down.failure_reason
                result = action_down.result
                print("Pickup Cube failed: code=%s reason='%s' result=%s" % (code, reason, result))
                return
            print("Cozmo successfully stacked 2 blocks!")
        else:
            print ("CUBES ARE NOT AVAILABLE")
            robot.play_anim_trigger(cozmo.anim.Triggers.MajorFail).wait_for_completed()

def cozmo_roll_cube(cube_to_roll, robot):
    print("COZMO TO ROLL CUBE %s" % str(cube_to_roll))
    cube_found = find_cube(cube_to_roll, robot)
    if cube_found:
        print ("CUBE FOUND!!")
        action = robot.roll_cube( cube_found, check_for_object_on_top=True, num_retries=2 )
        print("got action", action)
        result = action.wait_for_completed(timeout=30)
        print("got action result", result)
    else:
        print ("CUBE NOT Found")

def save_pose(save_pose_id, robot):
    current_pose=robot.pose
    global pose_dict
    pose_dict[save_pose_id] = current_pose

def remove_pose(save_pose_id, robot):
    print("REMOVING POSE")
    global pose_dict
    del pose_dict[save_pose_id]

def go_to_known_pose(save_pose_id, robot):
    print("GO TO KNOWN POSE")
    global pose_dict
    robot.go_to_pose(pose_dict.get(save_pose_id)).wait_for_completed()

# TO RENAME IN MY NEW ENVIRONMENT
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
class SnippetList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get_robot_context(self):
        print("Thread is open!")
        global robot
        cozmo.setup_basic_logging()
        try:
            cozmo.connect(run_robot, connector=cozmo.run.FirstAvailableConnector())
            print("Robot is ready now")
        except cozmo.ConnectionError as e:
            sys.exit("Connection Error: %s" % e)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        global robot
        if robot is None:
            # Create connection to cozmo
            print("Firs Call receive: Opening Cozmo Connectivity")
            thread = threading.Thread(target=self.get_robot_context, args=())
            thread.daemon = True
            thread.start()
        # Leemos los comandos, los parámetros y ejecutamos la orden.
        data = JSONParser().parse(request)
        print(data)
        if cozmo_is_busy:
            return JsonResponse("COZMO IS BUSY RIGHT NOW", status=200, safe=False)
        else:
            global commands_to_cozmo
            if commands_to_cozmo:
                print ("Commands Pending.... CHECK ERROR")
                return JsonResponse("COZMO HAS SOME COMMANDS PENDING", status=200, safe=False)
            else:
                commands_to_cozmo = data

        return JsonResponse("ACTION COMPLETED", status=200, safe=False)


class SnippetDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
