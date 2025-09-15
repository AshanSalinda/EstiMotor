from app.db.vehicle_data_repository import vehicle_data_repo

def get_similar_ads(vehicle: dict, limit: int = 8) -> list:
    """
    Find up to `limit` similar ads.
    Try strict match first, then relax (make+model), then (make),
    then fallback with no filters.
    """
    try:
        results = []
        seen_urls = set()

        # Prepare queries in priority order
        strict = {
            "make": vehicle.get("make"),
            "model": vehicle.get("model"),
            "fuel_type": vehicle.get("fuel_type"),
            "transmission": vehicle.get("transmission"),
        }
        make_model = {
            "make": vehicle.get("make"),
            "model": vehicle.get("model"),
        }
        make_only = {
            "make": vehicle.get("make"),
        }
        no_filter = {}

        for query in (strict, make_model, make_only, no_filter):
            if len(results) >= limit:
                break

            remaining = limit - len(results)
            docs = vehicle_data_repo.fetch_similar_ads(vehicle, query, remaining, seen_urls)

            if not docs:
                continue

            # Just in case, filter duplicates again
            new = []
            for d in docs:
                url = d.get("url")
                if url in seen_urls:
                    continue
                new.append(d)
                seen_urls.add(url)

            results.extend(new)

        # Format returned docs (strip internal fields)
        final = []
        for d in results[:limit]:
            final.append({
                "image": d.get("image"),
                "title": d.get("title"),
                "year": d.get("year"),
                "mileage": d.get("mileage"),
                "source": (d.get("url", "").split("/")[2]),
                "price": d.get("price"),
                "url": d.get("url")
            })

        return final

    except Exception as e:
        print("Error in get_similar_ads:", e)
        return []
