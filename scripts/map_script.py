import folium

from db.db_setup import SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.api.brewery.models import Brewery
from app.api.user.models import User


def get_data(session: Session):
    query = select(Brewery)
    result = session.execute(query)
    return result.scalars().all()


def create_map(data):
    m = folium.Map(location=(33.448376, -112.074036))

    for brewery in data:
        try:
            lat = float(brewery.latitude) if brewery.latitude else None
            lon = float(brewery.longitude) if brewery.longitude else None
        except ValueError:
            continue

        # Add marker if lat and lon are valid
        if lat is not None and lon is not None:
            folium.Marker(
                tooltip=f"{brewery.name} - {brewery.brewery_type}",
                location=[lat, lon],
                popup=(
                    f"{brewery.name}<br>"
                    f"Type: {brewery.brewery_type}<br>"
                    f"Address: {brewery.address}, {brewery.city}, {brewery.state_province}<br>"
                    f"Phone: {brewery.phone}<br>"
                    f"Website: <a href='{brewery.website_url}' target='_blank'>{brewery.website_url}</a>"
                ),
            ).add_to(m)

    m.save("brew_map.html")


def main():
    with SessionLocal() as session:
        data = get_data(session)
        create_map(data)


if __name__ == "__main__":
    main()
