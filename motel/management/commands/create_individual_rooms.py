from django.core.management.base import BaseCommand
from motel.models import Rooms, Room


class Command(BaseCommand):
    help = 'Create individual rooms for each room category based on number_of_rooms'

    def handle(self, *args, **kwargs):
        # Get all room categories
        room_categories = Rooms.objects.all()
        
        total_created = 0
        
        for category in room_categories:
            # Check how many individual rooms already exist for this category
            existing_rooms = Room.objects.filter(room_type=category).count()
            
            # Calculate how many more rooms need to be created
            rooms_to_create = category.number_of_rooms - existing_rooms
            
            if rooms_to_create > 0:
                # Get the highest room number for this category
                last_room = Room.objects.filter(room_type=category).order_by('-room_number').first()
                start_number = last_room.room_number + 1 if last_room else 1
                
                # Create the missing rooms
                rooms_list = []
                for i in range(rooms_to_create):
                    room = Room(
                        room_type=category,
                        room_number=start_number + i,
                        is_available=True
                    )
                    rooms_list.append(room)
                
                Room.objects.bulk_create(rooms_list)
                total_created += rooms_to_create
                self.stdout.write(self.style.SUCCESS(
                    f'Created {rooms_to_create} rooms for {category.room_name} '
                    f'(Room numbers {start_number}-{start_number + rooms_to_create - 1})'
                ))
            elif rooms_to_create < 0:
                self.stdout.write(self.style.WARNING(
                    f'{category.room_name}: Has {existing_rooms} rooms but number_of_rooms is {category.number_ofrooms}. '
                    f'Please update the number_of_rooms field or delete extra rooms manually.'
                ))
            else:
                self.stdout.write(f'{category.room_name}: Already has {existing_rooms} individual rooms')
        
        if total_created > 0:
            self.stdout.write(self.style.SUCCESS(f'Successfully created {total_created} individual rooms!'))
        else:
            self.stdout.write('All room categories already have the correct number of individual rooms.')

