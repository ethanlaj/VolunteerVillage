import BASE_URL from '.';

// Older Auth0 sessions can retain the Firebase picture URL after migration.
export function profilePictureUrl(picture) {
  if (!picture) return picture;
  try {
    const url = new URL(picture);
    const prefix = '/volunteer-village-94f65.appspot.com/profile_pictures/';
    if (url.hostname !== 'storage.googleapis.com' || !url.pathname.startsWith(prefix)) {
      return picture;
    }
    const userId = decodeURIComponent(url.pathname.slice(prefix.length));
    if (!userId || userId.includes('/') || userId.includes('\\')) return picture;
    return `${BASE_URL}profile/picture/${encodeURIComponent(userId)}`;
  } catch {
    return picture;
  }
}
