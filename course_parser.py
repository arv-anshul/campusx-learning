from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Iterable, Literal, Self

from bs4 import BeautifulSoup, Tag

if TYPE_CHECKING:
    from pathlib import Path

    import httpx

COURSE_URL = "https://learnwith.campusx.in/s/courses/653f50d1e4b0d2eae855480a/take"
BASE_RESOURCE_URL = "https://learnwith.campusx.in/s/courses/653f50d1e4b0d2eae855480a"
BASE_HEADERS = {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "referer": COURSE_URL,
    "user-agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_7) AppleWebKit/537.36 (KHTML, "
        "like Gecko) Chrome/111.5.0.0 Safari/507.02"
    ),
}
ResourceType = Literal[
    "article",
    "assessment",
    "assignment",
    "link",
    "livetest",
    "pdf",
    "video",
]


def fetch_sub_topic_resource(
    client: httpx.Client,
    sub_topic_id: str,
    resource_type: ResourceType,
) -> bytes:
    """Fetches the resource data for the given subtopic ID and resource type.

    Args:
        client: HTTPX client instance with cookies set.
        sub_topic_id: ID of the subtopic to fetch.
        resource_type: Type of resource to fetch.

    Returns:
        The data as bytes for the requested resource.

    Raises:
        ValueError: If client does not have cookies set.
        HTTPError: If the API request fails.
    """
    if not client.cookies:
        raise ValueError("Client does not have cookies.")
    res = client.get(f"/{resource_type}s/{sub_topic_id}/get")
    res.raise_for_status()
    return res.content


@dataclass(kw_only=True)
class CourseTopic:
    title: str
    id: str
    source: Tag = field(repr=False)

    @staticmethod
    def search(html_path: Path) -> Tag:
        """
        Parses CourseTopic instances from a BeautifulSoup tag.

        Yields CourseTopic instances parsed from the provided BeautifulSoup tag source.
        """
        soup = BeautifulSoup(html_path.read_bytes(), "html.parser")
        course_items_tag = soup.select_one("div.courseItems")
        if course_items_tag:
            return course_items_tag
        raise ValueError("'div.courseItems' css selector not present in source.")

    @classmethod
    def parse(cls, source: Tag) -> Iterable[Self]:
        """
        Parses CourseTopic instances from a BeautifulSoup tag.

        Yields CourseTopic instances parsed from the provided BeautifulSoup tag source.
        """
        yield from (
            cls(
                title=tag["data-title"],
                id=tag["data-id"],
                source=tag,
            )
            for tag in source.find_all("div", {"data-type": "label"})
        )


@dataclass(kw_only=True)
class CourseSubTopic:
    id: str
    topicId: str
    title: str
    type: ResourceType
    source: Tag = field(repr=False)

    @classmethod
    def parse(cls, topic: CourseTopic) -> Iterable[Self]:
        """
        Parses CourseSubTopic instances from a CourseTopic BeautifulSoup tag.

        Yields CourseSubTopic instances parsed from the provided CourseTopic
        BeautifulSoup tag source.
        """
        yield from (
            cls(
                id=tag["data-id"],
                topicId=topic.id,
                title=tag["data-title"],
                type=tag["data-type"],
                source=tag,
            )
            for tag in topic.source.find_all("div", {"data-type": True})
        )

    @classmethod
    def parse_many(
        cls,
        topics: Iterable[CourseTopic],
    ) -> Iterable[tuple[CourseTopic, Iterable[Self]]]:
        for topic in topics:
            yield topic, cls.parse(topic)

    @classmethod
    def find(
        cls,
        course_topics: Iterable[CourseTopic],
        *,
        id: str | None = None,
        title: str | None = None,
    ) -> Iterable[Self]:
        """
        Parses a single CourseSubTopic from the given CourseTopics.

        This allows fetching a specific CourseSubTopic by title or id from the
        list of CourseTopics, by searching through their associated subtopics.

        Args:
            course_topics: Iterable of CourseTopic instances to search through.
            title: Optional title of subtopic to find.
            id: Optional id of subtopic to find.

        Returns:
            Iterable of matching CourseSubTopic instances.

        Raises:
            ValueError: If both title and id are None.
            ValueError: If no matching subtopic is found.
        """
        if id is None and title is None:
            raise ValueError("Both 'id' and 'title' must not be None.")

        for topic in course_topics:
            if topic.id == id or topic.title == title:
                yield from cls.parse(topic)
                break
        else:
            raise ValueError(f"No subtopic found matching id={id} or title={title}")


@dataclass(kw_only=True)
class CourseVideoResource:
    id: str
    topicId: str
    title: str
    totalTime: str
    description: str = field(repr=False)
    isDescriptionHtml: bool = field(repr=False)

    @classmethod
    def fetch(cls, client: httpx.Client, sub_topic: CourseSubTopic) -> Self:
        if sub_topic.type != "video":
            raise ValueError(f"sub_topic is not a video resource, got {sub_topic.type}")

        response = fetch_sub_topic_resource(
            client=client,
            sub_topic_id=sub_topic.id,
            resource_type="video",
        )
        try:
            data = json.loads(response)
            data = data["spayee:resource"]
        except json.JSONDecodeError as e:
            raise ValueError("Response could not be parsed as JSON.") from e
        except KeyError as e:
            raise ValueError("Bad response or missing required fields.") from e
        return cls(
            id=sub_topic.id,
            topicId=sub_topic.topicId,
            title=data["spayee:title"],
            description=data["spayee:description"],
            totalTime=data["spayee:totalTime"],
            isDescriptionHtml=data["spayee:isDescriptionHtml"],
        )


@dataclass(kw_only=True)
class CourseAssignmentResource:
    id: str
    topicId: str
    title: str
    assignmentLink: str = field(repr=False)

    @classmethod
    def fetch(cls, client: httpx.Client, sub_topic: CourseSubTopic) -> Self:
        if sub_topic.type != "assignment":
            raise ValueError(
                f"sub_topic is not an assignment resource, got {sub_topic.type}"
            )

        response = fetch_sub_topic_resource(
            client=client,
            sub_topic_id=sub_topic.id,
            resource_type="assignment",
        )

        def parse_assignment_link(source: str | bytes) -> str:
            soup = BeautifulSoup(source, "html.parser")
            link_tag = soup.select_one("#instructions a")
            if link_tag:
                return link_tag.get_attribute_list("href", "")[0]
            raise ValueError("assignmentLink tag not found in source")

        return cls(
            id=sub_topic.id,
            topicId=sub_topic.topicId,
            title=sub_topic.title,
            assignmentLink=parse_assignment_link(response),
        )


if __name__ == "__main__":
    from pathlib import Path

    import httpx
    from rich import print

    # campusx.html contains the html content of the website
    course_topic_tag = CourseTopic.search(Path("campusx.html"))
    course_topics = list(CourseTopic.parse(course_topic_tag))
    print(course_topics[-10:])

    sub_topics = list(CourseSubTopic.find(course_topics, id="olh5gfqpjt"))
    print(list(sub_topics))

    # Fill cookies from browser's network tab
    cookies = {
        "c_ujwt": "Your Token",
        "SESSIONID": "Your current SESSION ID.",
    }

    results: list[CourseVideoResource] = []
    with httpx.Client(
        base_url=BASE_RESOURCE_URL, headers=BASE_HEADERS, cookies=cookies
    ) as client:
        for i, sub_topic in enumerate(sub_topics, 1):
            if sub_topic.type != "video":
                print(f"subtopic id={sub_topic.id} is not a video resource.")
                continue
            if i % 7 == 0:
                print("sleeping for 3 seconds...")
                time.sleep(3)
            results.append(CourseVideoResource.fetch(client, sub_topic))
    if not results:
        raise ValueError("No video resources found.")
    print(results)
