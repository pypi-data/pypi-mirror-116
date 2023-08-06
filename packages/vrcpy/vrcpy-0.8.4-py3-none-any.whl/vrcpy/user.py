from vrcpy.file import FileBase
from vrcpy.avatar import Avatar
from vrcpy.errors import ObjectErrors
from vrcpy.baseobject import BaseObject
from vrcpy.favorite import BaseFavorite
from vrcpy.favorite import FavoriteGroup
from vrcpy.permission import BasePermission
from vrcpy.moderation import PlayerModeration
from vrcpy.enum import FavoriteType, SortOrder, SortType, ReleaseStatus
import vrcpy.util

import logging
import json


class FriendStatus(BaseObject):
    def __init__(self, obj, user_id):
        super(None, None)

        self.required.update({
            "incoming_request": {
                "dict_key": "incomingRequest",
                "type": bool
            },
            "is_friend": {
                "dict_key": "isFriend",
                "type": bool
            },
            "outgoing_request": {
                "dict_key": "outgoingRequest",
                "type": bool
            }
        })

        self.user_id = user_id
        self._assign(obj)


class LimitedUser(BaseObject):
    def __init__(self, client, obj=None, loop=None):
        super().__init__(client, loop=loop)

        self.required.update({
            "username": {
                "dict_key": "username",
                "type": str
            },
            "display_name": {
                "dict_key": "displayName",
                "type": str
            },
            "id": {
                "dict_key": "id",
                "type": str
            },
            "avatar_image_url": {
                "dict_key": "currentAvatarImageUrl",
                "type": str
            },
            "avatar_thumbnail_url": {
                "dict_key": "currentAvatarThumbnailImageUrl",
                "type": str
            },
            "last_platform": {
                "dict_key": "last_platform",
                "type": str
            },
            "tags": {
                "dict_key": "tags",
                "type": list
            },
            "developer_type": {
                "dict_key": "developerType",
                "type": str
            },
            "is_friend": {
                "dict_key": "isFriend",
                "type": bool
            },
            "last_login": {
                "dict_key": "last_login",
                "type": str
            }
        })

        self.optional.update({
            "status": {
                "dict_key": "status",
                "type": str
            },
            "bio": {
                "dict_key": "bio",
                "type": str
            },
            "location": {
                "dict_key": "location",
                "type": str
            },
            "status_description": {
                "dict_key": "statusDescription",
                "type": str
            }
        })

        if obj is not None:
            self._assign(obj)

    async def fetch_full(self):
        '''
        Returns this user as a User object
        '''

        logging.debug("Getting User object of user " + self.username)

        return await self.client.fetch_user(self.id)

    async def fetch_friend_status(self):
        '''
        Gets friend request and is_friend status'
        Returns FriendStatus object
        '''

        logging.debug("Getting user status for " + self.id)

        friend_status = await self.client.request.get(
            "/user/%s/friendStatus" % self.id)
        return FriendStatus(friend_status["data"], self.id)

    async def send_friend_request(self):
        '''
        Sends a friend request notification to this user
        '''

        logging.debug("Sending friend request to " + self.username)

        if self.is_friend:
            raise ObjectErrors.AlreadyFriends(
                "You are already friends with " + self.display_name)

        await self.client.request.post(
            "/user/%s/friendRequest" % self.id)

    async def unfriend(self):
        '''
        Unfriends this user
        '''

        logging.debug("Unfriending user " + self.username)

        if not self.is_friend:
            raise ObjectErrors.NotFriends(
                "You are not friends with " + self.display_name)

        await self.client.request.delete(
            "/auth/user/friends/" + self.id)

    async def favorite(self, group):
        '''
        Favorite this user
        Returns a FriendFavorite object

            group, str
            Name of group to add friend to
        '''

        logging.debug("Favoriting user with id " + self.id)

        if not self.is_friend:
            raise ObjectErrors.NotFriends(
                "You are not friends with " + self.display_name)

        if group not in self.client.me.friend_group_names:
            raise ObjectErrors.InvalidGroupName(
                "Group name must be one of %s, not %s" % (
                    self.client.me.friend_group_names,
                    group
                )
            )

        resp = await self.client.request.post(
            "/favorites",
            params={
                "type": "friend",
                "favoriteId": self.id,
                "tags": [group]
            }
        )

        this = BaseFavorite.build_favorite(
            self.client, resp["data"], self.loop)
        self.client.favorites[FavoriteType.FRIEND].append(this)

        return this

    async def add_moderation(self, t):
        '''
        Adds a moderation against this user
        Returns a PlayerModeration

            t, str (use vrcpy.enum.PlayerModerationType for convenience)
            Type of moderation
        '''

        logging.debug("Adding moderations %s to user %s" % (
            t, self.id))

        moderation = await PlayerModeration.create_moderation(
            t, self.id, self.client, self.loop)

        return moderation


class User(LimitedUser):
    def __init__(self, client, obj=None, loop=None):
        super().__init__(client, loop=loop)

        '''
        self.required.update({

        })
        '''

        self.optional.update({
            "bio_links": {
                "dict_key": "bioLinks",
                "type": list
            },
            "state": {
                "dict_key": "state",
                "type": str
            },
            "friend_key": {
                "dict_key": "friendKey",
                "type": str
            },
            "world_id": {
                "dict_key": "worldId",
                "type": str
            },
            "instance_id": {
                "dict_key": "instanceId",
                "type": str
            },
            "allow_avatar_copying": {
                "dict_key": "allowAvatarCopying",
                "type": bool
            }
        })

        if obj is not None:
            self._assign(obj)


class CurrentUser(User):
    def __init__(self, client, obj, loop=None):
        super().__init__(client, loop=loop)

        self.required.update({
            "past_display_names": {
                "dict_key": "pastDisplayNames",
                "type": list
            },
            "email_verified": {
                "dict_key": "emailVerified",
                "type": bool
            },
            "has_email": {
                "dict_key": "hasEmail",
                "type": bool
            },
            "has_pending_email": {
                "dict_key": "hasPendingEmail",
                "type": bool
            },
            "accepted_tos_version": {
                "dict_key": "acceptedTOSVersion",
                "type": int
            },
            "has_birthday": {
                "dict_key": "hasBirthday",
                "type": bool
            },
            "friends": {
                "dict_key": "friends",
                "type": list
            },
            "online_friends": {
                "dict_key": "onlineFriends",
                "type": list
            },
            "active_friends": {
                "dict_key": "activeFriends",
                "type": list
            },
            "offline_friends": {
                "dict_key": "offlineFriends",
                "type": list
            },
            "friend_group_names": {
                "dict_key": "friendGroupNames",
                "type": list
            },
            "avatar": {
                "dict_key": "currentAvatar",
                "type": dict
            },
            "avatar_asset_url": {
                "dict_key": "currentAvatarAssetUrl",
                "type": str
            },
            "home_location": {
                "dict_key": "homeLocation",
                "type": str
            },
            "has_logged_in_from_client": {
                "dict_key": "hasLoggedInFromClient",
                "type": bool
            },
            "mfa_enabled": {
                "dict_key": "twoFactorAuthEnabled",
                "type": bool
            },
            "unsubscribe": {
                "dict_key": "unsubscribe",
                "type": bool
            }
        })

        self.optional.update({
            "email": {
                "dict_key": "email",
                "type": str
            },
            "obfuscated_email": {
                "dict_key": "obfuscatedEmail",
                "type": str
            },
            "obfuscated_pending_email": {
                "dict_key": "obfuscatedPendingEmail",
                "type": str
            },
            "steam_id": {
                "dict_key": "steamId",
                "type": str
            },
            "steam_details": {
                "dict_key": "steamDetails",
                "type": dict
            },
            "oculus_id": {
                "dict_key": "oculusId",
                "type": str
            },
            "account_deletion_date": {
                "dict_key": "accountDeletionDate",
                "type": str
            }
        })

        self._assign(obj)

    async def fetch_friends(self, offline=False, n=100, offset=0):
        '''
        Returns list of LimitedUser objects
        '''

        logging.debug(
            "Fetching %s friends" % "offline" if offline else "online")

        resp = await self.client.request.get(
            "/auth/user/friends", params={
                "offset": offset,
                "n": n,
                "offline": offline})

        return [LimitedUser(
            self.client, user, self.loop) for user in resp["data"]]

    async def fetch_permissions(self, condensed=False):
        '''
        Gets users permissions
        Returns list of different Permission objects

            condensed, bool
            Whether to return condensed perms or not
            If this is true then return will be a
                dict of single key-value pairs
        '''

        logging.debug("Getting permissions (%scondensed)" % (
            "" if condensed else "not "))

        if condensed:
            perms = await self.client.request.get(
                "/auth/permissions", params={"condensed": True})
            return perms["data"]
        else:
            perms = await self.client.request.get("/auth/permissions")
            return [BasePermission.build_permission(
                self.client, perm, self.loop) for perm in perms["data"]]

    async def fetch_favorites(self, favorite_type=None, n=100, offset=0):
        '''
        Fetches users favorites
        Returns list of different Favorite types

            favorite_type, str
            Type of enum.FavoriteType

            n, int
            Number of favorites to return, max 100

            offset, int
            Offset from start of favorites to return from
        '''

        if n > 100:
            n = 100

        params = {
            "n": n,
            "offset": offset
        }

        if favorite_type is not None:
            params["type"] = favorite_type

        favorites = await self.client.request.get("/favorites", params=params)
        logging.debug("Fetching favorites")

        return [BaseFavorite.build_favorite(
            self.client, favorite, self.loop) for favorite in favorites["data"]]

    async def fetch_all_favorites(self, favorite_type=None):
        '''
        Fetches all favorites by auto-paging
            Using this also updates favorite cache
        Returns list of different Favorite types

            favorite_type, str
            Type of enum.FavoriteType
        '''

        favorites = await vrcpy.util.auto_page_coro(
            self.fetch_favorites, favorite_type=favorite_type)

        world = []
        friend = []
        avatar = []

        for favorite in favorites:
            if favorite.type == FavoriteType.WORLD:
                world.append(favorite)
            elif favorite.type == FavoriteType.FRIEND:
                friend.append(favorite)
            elif favorite.type == FavoriteType.AVATAR:
                avatar.append(favorite)

        if world != []:
            self.client.favorites[FavoriteType.WORLD] = world
        if friend != []:
            self.client.favorites[FavoriteType.FRIEND] = friend
        if avatar != []:
            self.client.favorites[FavoriteType.AVATAR] = avatar

        return favorites

    async def fetch_notifications(self, type="all", sent=False, after=None):
        logging.debug("Fetching user notifications")

        params = {
            "type": type,
            "sent": sent
        }

        if after is not None:
            params["after"] = after

        notifs = await self.client.request.get("/auth/user/notifications")
        return [self.client.BaseNotification.build_notification(
            self.client, notif, self.loop) for notif in notifs["data"]]

    async def fetch_moderated(self):
        logging.debug("Fetching moderated")

        data = await self.client.request.get("/auth/user/playermoderated")
        return [PlayerModeration.build_moderation(
            self.client, mod, self.loop) for mod in data["data"]]

    async def fetch_files(self, tag=None, n=100):
        '''
        Gets user icons
        Returns list of IconFile objects

            tag, str
            Tag to filter files

            n, int
            Number of files to return (max might be 100?)
        '''

        logging.debug("Fetching files (tag is %s)" % tag)

        params = {"n": n}
        if tag is not None:
            params.update({"tag": tag})

        files = await self.client.request.get("/files", params=params)
        return [FileBase.build_file(
            self.client, file, self.loop) for file in files["data"]]

    async def fetch_avatars(self, sort: SortType = SortType.UPDATED,
                            order: SortOrder = SortOrder.DESCENDING,
                            release_status: ReleaseStatus = ReleaseStatus.ALL):
        '''
        Gets user avatars
        Returns list of Avatar objects

            sort, SortType
            What to sort avatars by

            order, SortOrder
            Order to sort in

            release_status, ReleaseStatus
            Release Status to filter avatars by
        '''

        avatars = await self.client.request.get("/avatars", params={
            "sort": sort.value,
            "order": order.value,
            "releaseStatus": release_status.value
        })
        return [Avatar(
            self.client, avatar, self.loop) for avatar in avatars["data"]]

    async def fetch_current_avatar(self):
        avatar = await self.client.request.get("/users/%s/avatar" % self.id)
        return Avatar(
            self.client, json.loads(avatar["data"]["success"]["message"]),
            self.loop)

    async def _update(self, **kwargs):
        for kwarg in kwargs:
            if kwargs[kwarg] is None:
                kwargs[kwarg] = getattr(self, kwarg)

        self.raw.update({
            "email": kwargs["email"],
            "birthday": kwargs["birthday"],
            "tags": kwargs["tags"],
            "status": kwargs["status"],
            "acceptedTOSVersion": kwargs["accepted_tos_version"],
            "allowAvatarCopying": kwargs["allow_avatar_copying"],
            "bio": kwargs["bio"],
            "bioLinks": kwargs["bio_links"]
        })

        logging.debug("Updating CurrentUser")

        me = await self.client.request.put("/users/"+self.id)
        self.client.me = CurrentUser(self.client, me["data"], self.loop)
        return self.client.me

    async def update(self, email=None, birthday=None, tags=None, status=None,
                     accepted_tos_version=None, allow_avatar_copying=None,
                     bio=None, bio_links=None):

        await self._update(email=email, birthday=birthday, tags=tags,
                           status=status, bio=bio, bio_Links=bio_links,
                           accepted_tos_version=accepted_tos_version,
                           allow_avatar_copying=allow_avatar_copying)

    async def fetch_favorite_groups(self, n: int = 50):
        '''
        Fetches favorite groups for worlds, avatars and users

            n, int
            Max number of favorites groups to fetch
        '''

        resp = await self.client.request.get("/favorite/groups", params={"n": str(n)})
        groups = {}

        for group in resp["data"]:
            groups.append(FavoriteGroup.build_favorite_group(
                self.client, group, self.loop))

        return groups