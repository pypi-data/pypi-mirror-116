from typing import Optional

from datetime import datetime

from ..core import BaseFlarumBulkObject, BaseFlarumIndividualObject
from ..core.discussions import DiscussionFromNotification
from ..core.users import UserFromNotification
from ..core.posts import PostFromNotification

from ...error_handler import parse_request
from ...datetime_conversions import flarum_to_datetime


class Notifications(BaseFlarumBulkObject):
    """
        A data of multiple notifications fetched from the API.
    """


    def __iter__(self):
        return iter(self.get_notifications())


    def get_notifications(self) -> list['Notification']:
        """
            All notifications from the `Notifications` object.
        """

        all_notifications = [] # type: list[Notification]

        for raw_notification in self.data:
            if raw_notification.get("type", None) == 'notifications':
                notification = Notification(user=self.user, _fetched_data=dict(data=raw_notification, _parent_included=self.included))
                all_notifications.append(notification)

        return all_notifications


    def mark_all_as_read(self) -> True:
        """
            Marks all notifications as read. Returns `True` when successful.
        """

        return super().user.mark_all_notifications_as_read()



class Notification(BaseFlarumIndividualObject):
    """
        Notification.
    """


    @property
    def contentType(self) -> Optional[str]:
        """
            The content type of the notification.

            Examples: `newPost`, `postLiked`, etc...
        """

        return self.attributes.get("contentType", None)


    @property
    def content(self) -> Optional[dict]:
        """
            The `dict` of the notification's content.
        """

        return self.attributes.get("content", None)


    @property
    def new_post_number(self) -> Optional[int]:
        """
            The new number of the potential post that triggered
            the notification.
        """

        if self.content and self.contentType == "newPost":
            post_number = self.content.get("postNumber", None)

            if post_number:
                return int(post_number)


    @property
    def reply_number(self) -> Optional[int]:
        """
            The number of the reply post that possibly triggered
            the notification.
        """

        if self.content and self.contentType == "postMentioned":
            reply_number = self.content.get("replyNumber", None)

            if reply_number:
                return int(reply_number)


    @property
    def createdAt(self) -> Optional[datetime]:
        """
            The `datetime` of when was this notification triggered/created at.
        """

        raw = self.attributes.get("createdAt", None)

        return flarum_to_datetime(raw)


    @property
    def isRead(self) -> bool:
        """
            Whether or not the notification was read by you.
        """

        return self.attributes.get("isRead", False)


    def from_user(self) -> Optional[UserFromNotification]:
        """
            From which user does the notification originate from?

            Returns `pyflarum.flarum.core.users.UserFromNotification`.
        """

        id = self.relationships.get("fromUser", {}).get("data", {}).get("id", None)
        
        for raw_user in self._parent_included:
            if raw_user.get("id", None) == id and raw_user.get("type", None) == 'users':
                user = UserFromNotification(user=self.user, _fetched_data=dict(data=raw_user))
                return user

        return None


    def get_subject(self) -> Optional['DiscussionFromNotification | PostFromNotification']:
        """
            Returns the subject of the notification, either one of these:
            - `pyflarum.flarum.core.discussions.DiscussionFromNotification`
            - `pyflarum.flarum.core.posts.PostFromNotification`
        """

        id = self.relationships.get("subject", {}).get("data", {}).get("id", None)
        
        for raw_subject in self._parent_included:
            if raw_subject.get("id", None) == id:
                notification_type = raw_subject.get("type", None)

                if notification_type == 'discussions':
                    return DiscussionFromNotification(user=self.user, _fetched_data=dict(data=raw_subject))

                elif notification_type == 'posts':
                    return PostFromNotification(user=self.user, _fetched_data=dict(data=raw_subject, _parent_included=self._parent_included))

        return None


    def mark_as_read(self) -> True:
        """
            Marks the notification as read.

            Returns `True` when successful.
        """

        post_data = {"is_read": True}
        raw = self.user.session.patch(f"{self.user.api_urls['notifications']}/{self.id}", json=post_data)
        parse_request(raw)

        return True
