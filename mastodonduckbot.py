#!/usr/bin/python3

# Copyright (C) 2024 Vivia Nikolaidou <vivia AT ahiru.eu>
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <https://www.gnu.org/licenses/>.

import os

import requests
from mastodon import Mastodon

duck_url = "https://random-d.uk/api/v2/random"


def main():
    """Post random duck pictures from the above API to Mastodon."""
    mastodon = Mastodon(
        api_base_url="https://toot.cat",
        access_token=os.environ["MASTODON_TOKEN"],
    )
    resp = requests.get(duck_url, timeout=10)
    resp.raise_for_status()

    resp_data = resp.json()
    image_url = resp_data["url"]
    image_resp = requests.get(image_url, stream=True, timeout=10)
    image_resp.raise_for_status()

    image_resp.raw.decode_content = True
    mime_type = image_resp.headers["Content-Type"]
    image_comment = resp_data["message"]
    media = mastodon.media_post(
        image_resp.raw,
        mime_type=mime_type,
        description="A random duck picture",
        synchronous=True,
    )
    mastodon.status_post(image_comment, media_ids=media)


if __name__ == "__main__":
    main()
