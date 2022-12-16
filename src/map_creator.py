from PIL import Image

def create_mask_map(m_path, ao_path, d_path, s_path):

    sizes = []

    if m_path != "":
        metallic_image = Image.open(m_path)
        sizes.append(metallic_image.size)
    else:
        metallic_image = None
    if ao_path != "":
        occlusion_image = Image.open(ao_path)
        sizes.append(occlusion_image.size)
    else:
        occlusion_image = None
    if d_path != "":
        detail_image = Image.open(d_path)
        sizes.append(detail_image.size)
    else:
        detail_image = None
    if s_path != "":
        smoothness_image = Image.open(s_path)
        sizes.append(smoothness_image.size)
    else:
        smoothness_image = None

    empty_placeholder = Image.new(mode="RGBA", size=sizes[0], color=(0, 0, 0, 0))
    alpha_placeholder = Image.new(mode="RGBA", size=sizes[0], color=(255, 255, 255, 255))

    if metallic_image is None:
        metallic_image = empty_placeholder
    if occlusion_image is None:
        occlusion_image = empty_placeholder
    if detail_image is None:
        detail_image = alpha_placeholder
    if smoothness_image is None:
        smoothness_image = alpha_placeholder

    return Image.merge("RGBA", (metallic_image.convert("L"), occlusion_image.convert("L"), detail_image.convert("L"), smoothness_image.convert("L")))

