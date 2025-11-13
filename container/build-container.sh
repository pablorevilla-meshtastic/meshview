#!/bin/sh
#
# build-container.sh
#
# Script to build MeshView container images

set -e

# Default values
IMAGE_NAME="meshview"
TAG="latest"
CONTAINERFILE="Containerfile"

# Parse arguments
while [ $# -gt 0 ]; do
    case "$1" in
        --tag|-t)
            TAG="$2"
            shift 2
            ;;
        --name|-n)
            IMAGE_NAME="$2"
            shift 2
            ;;
        --file|-f)
            CONTAINERFILE="$2"
            shift 2
            ;;
        --help|-h)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  -t, --tag TAG         Tag for the image (default: latest)"
            echo "  -n, --name NAME       Image name (default: meshview)"
            echo "  -f, --file FILE       Containerfile path (default: Containerfile)"
            echo "  -h, --help            Show this help"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

echo "Building MeshView container image..."
echo "  Image: ${IMAGE_NAME}:${TAG}"
echo "  Containerfile: ${CONTAINERFILE}"
echo ""

# Build the container
docker build -f "${CONTAINERFILE}" -t "${IMAGE_NAME}:${TAG}" .

echo ""
echo "Build complete!"
echo "Run with: docker run --rm -p 8081:8081 ${IMAGE_NAME}:${TAG}"
