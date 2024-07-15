import json
from ui.character import Character

character_data = {
    "character_1": {
        "name": "character_1",
        "image_paths": [
            "resources/images/character_1/2.png",
            "resources/images/character_1/3.png",
            "resources/images/character_1/4_1.png",
            "resources/images/character_1/5.png",
            "resources/images/character_1/6.png",
            "resources/images/character_1/7.png",
            "resources/images/character_1/8.png",
            "resources/images/character_1/9.png",
            "resources/images/character_1/10.png",
            "resources/images/character_1/11.png",
            "resources/images/character_1/12.png",
        ],
        "thresholds": [450, 1000, 2200, 4000, 9000, 19000, 40000, 90000, 200000, 600000, 2000000],
        "variant_images": {
            3: [
                "resources/images/character_1/5.png",
                "resources/images/character_1/5(1).png",
                "resources/images/character_1/5(2).png",
                "resources/images/character_1/5(3).png",
                "resources/images/character_1/5(4).png",
            ],
            4: [
                "resources/images/character_1/6.png",
                "resources/images/character_1/6(1).png",
                "resources/images/character_1/6(2).png",
                "resources/images/character_1/6(3).png",
                "resources/images/character_1/6(4).png",
                "resources/images/character_1/6(5).png",
                "resources/images/character_1/6(6).png",
                "resources/images/character_1/6(7).png",
                "resources/images/character_1/6(8).png",
            ],
            5: [
                "resources/images/character_1/7.png",
                "resources/images/character_1/7(1).png",
                "resources/images/character_1/7(2).png",
                "resources/images/character_1/7(3).png",
                "resources/images/character_1/7(4).png",
                "resources/images/character_1/7(5).png",
                "resources/images/character_1/7(6).png",
                "resources/images/character_1/7(7).png",
                "resources/images/character_1/7(8).png",
            ],
            6: [
                "resources/images/character_1/8_1.png",
            ],
            7: [
                "resources/images/character_1/9.png",
                "resources/images/character_1/9(1).png",
            ],
            8: [
                "resources/images/character_1/10.png",
                "resources/images/character_1/10(1).png",
            ],
            9: [
                "resources/images/character_1/11_1.png",
            ],
            10: [
                "resources/images/character_1/12.png",
            ]
        }
    },
    "character_2": {
        "name": "character_2",
        "image_paths": [
            "resources/images/character_2/1.png",
            "resources/images/character_2/2.png",
            "resources/images/character_2/3.png",
            "resources/images/character_2/4.png",
        ],
        "thresholds": [10, 10, 10, 10],
        "variant_images": {
            3: [
                "resources/images/character_1/4.png",
                "resources/images/character_1/4(1).png",
                "resources/images/character_1/4(2).png",
            ],
        }
    },
    "character_3": {
        "name": "character_3",
        "image_paths": [
            "resources/images/character_3/1.png",
            "resources/images/character_3/2.png",
            "resources/images/character_3/3.png",
            "resources/images/character_3/4.png",
            "resources/images/character_3/5.png",
            "resources/images/character_3/6.png",
            "resources/images/character_3/7.png",
            "resources/images/character_3/8.png",
            "resources/images/character_3/9.png",
            "resources/images/character_3/10_3.png",
        ],
        "thresholds": [450, 1000, 2000, 3500, 7200, 15000, 35000, 90000, 200000, 600000],
        "variant_images": {
            3: [
                "resources/images/character_3/4.png",
                "resources/images/character_3/4(1).png",
                "resources/images/character_3/4(2).png",
            ],
            4: [
                "resources/images/character_3/5.png",
                "resources/images/character_3/5(1).png",
                "resources/images/character_3/5(2).png",
                "resources/images/character_3/5(3).png",
            ],
            5: [
                "resources/images/character_3/6.png",
                "resources/images/character_3/6(1).png",
                "resources/images/character_3/6(2).png",
                "resources/images/character_3/6(3).png",
                "resources/images/character_3/6(4).png",
            ],
            6: [
                "resources/images/character_3/7.png",
                "resources/images/character_3/7(1).png",
                "resources/images/character_3/7(2).png",
                "resources/images/character_3/7(3).png",
            ],
            7: [
                "resources/images/character_3/8.png",
                "resources/images/character_3/8(1).png",
                "resources/images/character_3/8(2).png",
                "resources/images/character_3/8(3).png",
            ],
            8: [
                "resources/images/character_3/9.png",
                "resources/images/character_3/9(1).png",
            ],
            9: [
                "resources/images/character_3/10_3.png",
            ],
        }
    }
}
