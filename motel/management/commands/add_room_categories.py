from django.core.management.base import BaseCommand
from motel.models import Rooms


class Command(BaseCommand):
    help = 'Add premium Indian hotel room categories'

    def handle(self, *args, **kwargs):
        room_categories = [
            {
                'room_name': 'Deluxe Room',
                'room_des': 'A comfortable and well-appointed deluxe room featuring modern amenities, perfect for business and leisure travelers. The room offers a queen-size bed, work desk, and en-suite bathroom with premium toiletries.',
                'room_price': 4500,
                'room_facilities': 'WiFi, LED TV, AC, Mini Bar, Coffee Maker, Safe, Iron, Room Service',
                'room_image': 'rooms/room-1.jpg',
                'number_of_rooms': 15,
            },
            {
                'room_name': 'Premium Deluxe Room',
                'room_des': 'Elevated comfort with additional space and premium furnishings. Features a king-size bed, separate sitting area, and upgraded bathroom amenities. Perfect for guests seeking extra comfort.',
                'room_price': 6500,
                'room_facilities': 'WiFi, Smart TV, AC, Mini Bar, Coffee Maker, Safe, Iron, Bathrobes, Slippers, Room Service',
                'room_image': 'rooms/room-2.jpg',
                'number_of_rooms': 10,
            },
            {
                'room_name': 'Executive Room',
                'room_des': 'Designed for business travelers with dedicated workspace, high-speed internet, and access to the executive lounge. Features premium bedding and modern business amenities.',
                'room_price': 8000,
                'room_facilities': 'High-Speed WiFi, Smart TV, AC, Mini Bar, Coffee Maker, Safe, Iron, Work Desk, Executive Lounge Access',
                'room_image': 'rooms/room-3.jpg',
                'number_of_rooms': 8,
            },
            {
                'room_name': 'Junior Suite',
                'room_des': 'Spacious suite with a separate living area and bedroom. Ideal for families or guests wanting extra space. Features premium amenities and luxurious bedding.',
                'room_price': 10000,
                'room_facilities': 'WiFi, Smart TV, AC, Mini Bar, Coffee Maker, Safe, Iron, Living Area, Bathtub, Room Service',
                'room_image': 'rooms/room-4.jpg',
                'number_of_rooms': 6,
            },
            {
                'room_name': 'Executive Suite',
                'room_des': 'Luxurious suite featuring a master bedroom, separate living room, dining area, and pantry. Premium amenities with butler service available. The ultimate in comfort and style.',
                'room_price': 15000,
                'room_facilities': 'High-Speed WiFi, Smart TV, AC, Mini Bar, Premium Coffee Maker, Safe, Iron, Living Room, Dining Area, Bathtub, Butler Service',
                'room_image': 'rooms/room-5.jpg',
                'number_of_rooms': 4,
            },
            {
                'room_name': 'Presidential Suite',
                'room_des': 'The pinnacle of luxury living. This expansive suite features multiple bedrooms, grand living room, private dining room, personal kitchen, and panoramic views. Exclusive amenities and 24/7 butler service.',
                'room_price': 50000,
                'room_facilities': 'High-Speed WiFi, Multiple Smart TVs, AC, Full Bar, Premium Coffee Maker, Safe, Iron, Multiple Bathrooms, Living Room, Dining Room, Private Kitchen, Jacuzzi, Butler Service',
                'room_image': 'rooms/room-6.jpg',
                'number_of_rooms': 1,
            },
            {
                'room_name': 'Family Room',
                'room_des': 'Spacious room designed for families, featuring connecting rooms or extra bedding options. Child-friendly amenities and facilities ensure a comfortable stay for the whole family.',
                'room_price': 7500,
                'room_facilities': 'WiFi, LED TV, AC, Mini Bar, Coffee Maker, Safe, Iron, Extra Bedding, Kids Toys, Baby Cot, Room Service',
                'room_image': 'rooms/room-7.jpg',
                'number_of_rooms': 5,
            },
        ]

        for room_data in room_categories:
            room, created = Rooms.objects.get_or_create(
                room_name=room_data['room_name'],
                defaults=room_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created: {room.room_name}'))
            else:
                self.stdout.write(f'Already exists: {room.room_name}')

        self.stdout.write(self.style.SUCCESS('Successfully added all room categories!'))

