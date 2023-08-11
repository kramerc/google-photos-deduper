interface BaseMessageType {
  app: "GooglePhotosDeduper";
  action:
    | "healthCheck"
    | "healthCheck.result"
    | "deletePhoto"
    | "deletePhoto.result"
    | "startDeletionTask"
    | "startDeletionTask.result";
}

export interface HealthCheckMessageType extends BaseMessageType {
  action: "healthCheck";
}

export interface HealthCheckResultMessageType extends BaseMessageType {
  action: "healthCheck.result";
  success: true;
  version: string;
}

export interface StartDeletionTaskMessageType extends BaseMessageType {
  action: "startDeletionTask";
  mediaItems: {
    id: string;
    productUrl: string;
  }[];
}

export interface StartDeletionTaskResultMessageType extends BaseMessageType {
  action: "startDeletionTask.result";
  success: true;
}

export interface DeletePhotoMessageType extends BaseMessageType {
  action: "deletePhoto";
  mediaItemId: string;
}

export type DeletePhotoResultMessageType = BaseMessageType & {
  action: "deletePhoto.result";
  mediaItemId: string;
  originalMessage: DeletePhotoMessageType;
} & (
    | {
        success: true;
        deletedAt: Date;
        userUrl: URL;
      }
    | {
        success: false;
        error: string;
      }
  );

export type MessageType =
  | HealthCheckMessageType
  | HealthCheckResultMessageType
  | StartDeletionTaskMessageType
  | StartDeletionTaskResultMessageType
  | DeletePhotoMessageType
  | DeletePhotoResultMessageType;