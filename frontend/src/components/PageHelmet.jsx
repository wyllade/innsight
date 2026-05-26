import { Helmet } from "react-helmet-async";

const SITE_URL = import.meta.env.VITE_SITE_URL || "https://innsight.app";

export default function PageHelmet({
  title,
  description = "Find hotels by the life you want to live. Search by amenities, not just addresses.",
  image = "/og-image.png",
  url = SITE_URL,
  jsonLd,
}) {
  const fullTitle = title ? `${title} | Innsight` : "Innsight — Smarter Hotel Discovery";

  return (
    <Helmet>
      <title>{fullTitle}</title>
      <meta property="og:title" content={fullTitle} />
      <meta name="twitter:title" content={fullTitle} />
      {description && (
        <>
          <meta name="description" content={description} />
          <meta property="og:description" content={description} />
          <meta name="twitter:description" content={description} />
        </>
      )}
      <meta property="og:image" content={image} />
      <meta name="twitter:image" content={image} />
      <meta property="og:url" content={url} />
      {jsonLd && (
        <script type="application/ld+json">{JSON.stringify(jsonLd)}</script>
      )}
    </Helmet>
  );
}
